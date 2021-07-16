from abc import ABC

import pandas as pd

from import_module.model.file_import_configuration import FileImportConfiguration


class BaseValueResolver(ABC):

    def resolve_value(self, filename: str, df: pd.DataFrame, field_configuration: dict,
                      result_df: pd.DataFrame):
        pass

    def resolve_dataframe_filter(self, field_configuration: dict):
        condition = []
        for query in field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_DATAFRAME_QUERY):
            if query.get('cmaparison') == 'gte':
                condition.append(f'{query["name"]} >= {query["value"]}')
            elif query.get('cmaparison') == 'gt':
                condition.append(f'{query["name"]} > {query["value"]}')
            elif query.get('cmaparison') == 'lt':
                condition.append(f'{query["name"]} < {query["value"]}')
            elif query.get('cmaparison') == 'lte':
                condition.append(f'{query["name"]} <= {query["value"]}')
        return ' & '.join(condition)
