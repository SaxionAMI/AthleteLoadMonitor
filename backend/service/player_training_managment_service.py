from service.connection_service import ConnectionService
from pymongo.collection import Collection
from bson import ObjectId
from flask_jwt_extended import current_user


class PlayerTrainingManagementService:
    def __init__(self, connection_service: ConnectionService):
        self.connection_service = connection_service

    def get_unmapped_players_from_trainings(self):
        return self.__get_unmapped_training_connection().distinct('player_name', {'player_id': None})

    def delete_unmapped_player(self, player_name: str):
        self.__get_unmapped_training_connection().delete_many({'player_name': player_name})

    def __get_training_connection(self) -> Collection:
        return self.connection_service.get_connection_by_club_id(ObjectId(current_user['club_ids'][0])).db.training

    def __get_unmapped_training_connection(self) -> Collection:
        return self.connection_service.get_connection_by_club_id(ObjectId(current_user['club_ids'][0]))\
            .db.unmapped_training_record


