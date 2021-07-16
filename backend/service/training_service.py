from bson import ObjectId
from flask_jwt_extended import current_user
from pymongo.collection import Collection

from service.connection_service import ConnectionService


class TrainingService:
    def __init__(self, connection_service: ConnectionService):
        self.connection_service = connection_service

    def get_player_trainings(self, player_id:str):
        return list(self.__get_connection().training.find({'player_id': ObjectId(player_id)}).sort('timestamp', -1).limit(250))

    def get_player_training_averages(self, player_id: str):
        configurations = self.get_configuration()
        grouping_query = {'_id': '$player_id'}
        for config in configurations:
            grouping_query[config['average']] = {'$avg': f'${config["actual"]}'}

        return list(self.__get_connection().training.aggregate([
            {"$match": {"player_id": ObjectId(player_id)}},
            {"$group": grouping_query}])).pop()

    def get_configuration(self):
        return [self.__convert_to_configuration_dto(v) for v in
                self.__get_connection().ml_configuration.find({}, {'training_fields': 0})]

    def __convert_to_configuration_dto(self, value: dict) -> dict:
        result = {}
        result['predicted'] = value.get('predicted_value_name')
        result['actual'] = value.get('training_label_field')
        result['label'] = value.get('display_label')
        result['average'] = value.get('avg_field')
        return result

    def __get_connection(self) -> Collection:
        return self.connection_service.get_connection_by_club_id(ObjectId(current_user['club_ids'][0])).db
