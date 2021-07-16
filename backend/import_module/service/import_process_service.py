import json
from typing import List

import time
from bson import ObjectId
from flask_jwt_extended import current_user
from werkzeug.datastructures import FileStorage
import pandas as pd

from import_module.data_preprocessor.base_preprocessor import BasePreprocessor
from import_module.data_preprocessor.combine_exact_polar_time_preprocessor import CombineExactPolarTimePreprocessor
from import_module.data_preprocessor.delta_value_preprocessor import DeltaValuePreprocessor
from import_module.data_preprocessor.fill_na_preprocessor import FillNaPreprocessor
from import_module.model.file_import_configuration import FileImportConfiguration
from import_module.value_resolver.base_value_resolver import BaseValueResolver
from import_module.value_resolver.combined_value_resolver.action_count_resolver import ActionCountResolver
from import_module.value_resolver.combined_value_resolver.average_value_resolver import AverageValueResolver
from import_module.value_resolver.combined_value_resolver.calculated_average_value_resolver import \
    CalculatedAverageValueResolver
from import_module.value_resolver.combined_value_resolver.distance_value_resolver import DistanceValueResolver
from import_module.value_resolver.combined_value_resolver.first_timestamp_body_resolver import \
    FirstTimestampBodyResolver
from import_module.value_resolver.combined_value_resolver.hr_zone_value_resolver import HrZoneValueResolver
from import_module.value_resolver.combined_value_resolver.load_value_resolver import LoadValueResolver
from import_module.value_resolver.combined_value_resolver.max_min_difference_value_resolver import \
    MaxMinDifferenceValueResolver
from import_module.value_resolver.combined_value_resolver.total_duration_value_resolver import \
    TotalDurationValueResolver
from import_module.value_resolver.from_file_name_value_resolver import FromFileNameValueResolver
from import_module.value_resolver.timestamp_body_resolver import TimestampBodyResolver
from import_module.value_resolver.value_body_resolver import ValueBodyResolver
from service.connection_service import ConnectionService

# 38 s SRpe
class ImportProcessService:
    def __init__(self, connection_service: ConnectionService):
        self.connection_service = connection_service

    def import_data(self, configuration_id: str, files: List[FileStorage]):
        start = time.time()
        import_configuration = FileImportConfiguration.from_dict(
            self.__get_connection_db().file_import_configuration.find_one({'_id': ObjectId(configuration_id)}))
        for file in files:
            values = self.__resolve_values(import_configuration, file)
            player_name_id_map = self.__get_player_name_id_map(list(set(dic['player_name'] for dic in values)))
            for value in values:
                self.__map_values_if_possible(value, import_configuration, player_name_id_map)
        print(time.time() - start)

    def update_unmapped_player(self, player_name: str):
        unmapped_values = self.__get_connection_db().unmapped_training_record.find({'player_name': player_name})
        for value in unmapped_values:
            self.__get_connection_db().unmapped_training_record.delete_one({'_id': value['_id']})
            import_configuration = FileImportConfiguration.from_dict(
                self.__get_connection_db().file_import_configuration
                    .find_one({'_id': ObjectId(value['configuration_id'])}))
            del value['configuration_id']
            del value['_id']
            player_name_id_map = self.__get_player_name_id_map([player_name])
            self.__map_values_if_possible(value, import_configuration, player_name_id_map)

    def __resolve_values(self, import_configuration: FileImportConfiguration, file: FileStorage):
        import_preprocessing_list = import_configuration.get_preprocessors()
        field_configuration_list = import_configuration.get_fields()
        df = self.__load_file(import_configuration, file)
        for preprocessor in import_preprocessing_list:
            self.__get_preprocessor(preprocessor).execute(df, file.filename, preprocessor)
        result_df = pd.DataFrame()
        from_filename_configuration_list = []
        for field_configuration in field_configuration_list:
            resolver = self.__get_value_resolver(field_configuration)
            if not field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_FROM_BODY):
                from_filename_configuration_list.append(field_configuration)
            else:
                resolver.resolve_value(file.filename, df, field_configuration, result_df)

        for field_configuration in from_filename_configuration_list:
            resolver = self.__get_value_resolver(field_configuration)
            resolver.resolve_value(file.filename, df, field_configuration, result_df)
        return json.loads(result_df.to_json(orient="records"))

    def __map_values_if_possible(self, value, import_configuration: FileImportConfiguration, player_name_id_map: dict):
        is_mapped = self.__map_to_player(value, player_name_id_map)
        if not is_mapped:
            value['configuration_id'] = import_configuration.get_id()
            self.__get_connection_db().unmapped_training_record.insert_one(value)
        else:
            is_connected = self.__connect_to_existing_training(value, import_configuration)
            if not is_connected and import_configuration.create_new_if_not_mapped():
                self.__get_connection_db().training.insert_one(value)
            elif not is_connected:
                value['configuration_id'] = import_configuration.get_id()
                self.__get_connection_db().unmapped_training_record.insert_one(value)

    def __map_to_player(self, value, player_name_id_map: dict) -> bool:
        if player_name_id_map.get(value['player_name']) is not None:
            value['player_id'] = player_name_id_map.get(value['player_name'])
            return True
        return False

    def __connect_to_existing_training(self, value, configuration: FileImportConfiguration) -> bool:
        res = self.__get_connection_db().training.update_many(self.__create_mapping_query(configuration, value), {'$set': value})
        return res.modified_count > 0

    def __create_mapping_query(self, import_configuration: FileImportConfiguration, value):
        query = {}
        for mapping_config in import_configuration.get_mapping_fields():
            if mapping_config.get(FileImportConfiguration.ATTR_MAPPING_FIELD_TOLERANCE_S) == 0:
                query[mapping_config.get(FileImportConfiguration.ATTR_MAPPING_FIELD_NAME)] \
                    = value[mapping_config.get(FileImportConfiguration.ATTR_MAPPING_FIELD_NAME)]
            else:
                query['$and'] = [
                    {
                        mapping_config.get(FileImportConfiguration.ATTR_MAPPING_FIELD_NAME): {
                            '$gte': value[mapping_config.get(FileImportConfiguration.ATTR_MAPPING_FIELD_NAME)] - mapping_config.get(FileImportConfiguration.ATTR_MAPPING_FIELD_TOLERANCE_S)
                        }
                    },
                    {
                        mapping_config.get(FileImportConfiguration.ATTR_MAPPING_FIELD_NAME): {
                            '$lt': value[mapping_config.get(FileImportConfiguration.ATTR_MAPPING_FIELD_NAME)] + mapping_config.get(FileImportConfiguration.ATTR_MAPPING_FIELD_TOLERANCE_S)
                        }
                    }
                ]
        return query

    def __get_value_resolver(self, field_configuration: dict) -> BaseValueResolver:
        if field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'FileNameValueResolver':
            return FromFileNameValueResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'TimestampBodyResolver':
            return TimestampBodyResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'FirstTimestampBodyResolver':
            return FirstTimestampBodyResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'ValueBodyResolver':
            return ValueBodyResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'ActionCountResolver':
            return ActionCountResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'AverageValueResolver':
            return AverageValueResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'CalculatedAverageValueResolver':
            return CalculatedAverageValueResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'DistanceValueResolver':
            return DistanceValueResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'HrZoneValueResolver':
            return HrZoneValueResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'LoadValueResolver':
            return LoadValueResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'MaxMinDifferenceValueResolver':
            return MaxMinDifferenceValueResolver()
        elif field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_RESOLVER) == 'TotalDurationValueResolver':
            return TotalDurationValueResolver()
        else:
            raise Exception(f'Could not resolve value resolver{field_configuration.get_value_resolver()}')

    def __get_preprocessor(self, import_preprocessor: dict) -> BasePreprocessor:
        if import_preprocessor.get(FileImportConfiguration.ATTR_PREPROCESSOR) == 'CombineExactPolarTimePreprocessor':
            return CombineExactPolarTimePreprocessor()
        elif import_preprocessor.get(FileImportConfiguration.ATTR_PREPROCESSOR) == 'DeltaValuePreprocessor':
            return DeltaValuePreprocessor()
        elif import_preprocessor.get(FileImportConfiguration.ATTR_PREPROCESSOR) == 'FillNaPreprocessor':
            return FillNaPreprocessor()
        else:
            raise Exception(f'Could not resolve value preprocessor {import_preprocessor.get_preprocessor()}')

    def __get_player_name_id_map(self, needed_names: List[str]) -> dict:
        player_list = self.__get_connection_db().player.find({'name_variations': {'$elemMatch': {'$in': needed_names}}},
                                                             {'_id': 1, 'name_variations': 1})
        res = {}
        for player in player_list:
            for name in player['name_variations']:
                res[name] = player['_id']
        return res

    def __load_file(self, import_configuration: FileImportConfiguration, file: FileStorage):
        if import_configuration.get_extension() == '.csv':
            return pd.read_csv(file)
        elif import_configuration.get_extension() == '.xlsx':
            return pd.read_excel(file)
        else:
            raise Exception(f"File reader for type \"{import_configuration.get_extension()}\" is not configured")

    def __get_connection_db(self):
        return self.connection_service.get_connection_by_club_id(ObjectId(current_user['club_ids'][0])).db




