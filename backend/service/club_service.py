from typing import List

from bson import ObjectId
from flask_jwt_extended import current_user
from pymongo.collection import Collection

from model.club import Club
from service.connection_service import ConnectionService
from service.user_service import UserService


class ClubService:
    def __init__(self, club_collection: Collection, base_database_url: str,
                 user_service: UserService, connection_service: ConnectionService):
        self.club_collection = club_collection
        self.base_database_url = base_database_url
        self.user_service = user_service
        self.connection_service = connection_service

    def add(self, club: Club) -> str:
        database_url = f"{self.base_database_url}{club.get_name().replace(' ', '_').lower()}"
        club.set_database_url(database_url)
        new_club_id = self.club_collection.insert_one(club.get_dict_value()).inserted_id
        self.user_service.add_club_to_user(current_user['_id'], new_club_id)
        self.connection_service.update_connection_map()
        return new_club_id

    def delete(self, club_id: str) -> None:
        self.club_collection.delete_one({'_id': ObjectId(club_id)})
        self.connection_service.drop_db(ObjectId(club_id))
        self.user_service.delete_common_users_with_club_id(club_id)
        self.user_service.remove_club_from_users(club_id)
        self.connection_service.update_connection_map()

    def edit(self, club: Club) -> None:
        club_id = club.get_id()
        club.set_id(None)
        self.club_collection.update_one({'_id': ObjectId(club_id)}, {'$set': club.get_dict_value()})

    def get_one(self, club_id: str) -> Club:
        return Club.from_dict(self.club_collection.find_one({'_id': ObjectId(club_id)}))

    def get_all(self) -> List[Club]:
        return [Club.from_dict(doc) for doc in self.club_collection.find({}, {'database_url': 0})]

    def update_predictions(self, club_id):
        return {}
