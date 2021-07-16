from typing import List

from bson import ObjectId
from flask_jwt_extended import current_user
from pymongo.collection import Collection

from model.team import Team
from model.user import User
from service.connection_service import ConnectionService
from service.user_service import UserService


class TeamService:
    def __init__(self, connection_service: ConnectionService, user_service: UserService):
        self.connection_service = connection_service
        self.user_service = user_service

    def add(self, team: Team) -> str:
        new_team_id = self.__get_connection().insert_one(team.get_dict_value()).inserted_id
        self.user_service.add_team_to_user(current_user['_id'], new_team_id)
        return new_team_id

    def delete(self, team_id: str) -> None:
        team = self.get_team_by_id(team_id)
        if len(team.get_player_ids()) != 0:
            raise Exception('Team still has players associated with it. move or delete players before deleting team')
        self.user_service.remove_team_from_users(team_id)
        self.__get_connection().delete_one({'_id': ObjectId(team_id)})

    def edit(self, team: Team) -> None:
        team_id = team.get_id()
        team.set_id(None)
        self.__get_connection().update_one({'_id': ObjectId(team_id)}, {'$set': team.get_dict_value()})

    def get_all(self) -> List[Team]:
        return [Team.from_dict(doc) for doc in self.__get_connection().find({'_id': {'$in': current_user['team_ids']}})]

    def get_team_by_id(self, team_id: str) -> Team:
        team_dict = self.__get_connection().find_one({'_id': ObjectId(team_id)})
        return Team.from_dict(team_dict) if team_dict is not None else None

    def connect_trainer(self, trainer_id: str, team_id: str) -> None:
        user = User.from_dict(self.user_service.get_user_by_id(trainer_id))
        team = self.get_team_by_id(team_id)
        if user.get_club_ids()[0] == current_user['club_ids'][0] and user.get_role() == 2 and team is not None:
            self.user_service.add_team_to_user(trainer_id, team_id)
        else:
            raise Exception('Club admin can only connect trainers that are from the same club')

    def disconnect_trainer(self, trainer_id: str, team_id: str) -> None:
        user = User.from_dict(self.user_service.get_user_by_id(trainer_id))
        team = self.get_team_by_id(team_id)
        if user.get_club_ids()[0] == current_user['club_ids'][0] and user.get_role() == 2 and team is not None:
            self.user_service.remove_team_from_user(trainer_id, team_id)
        else:
            raise Exception('Club admin can only disconnect trainers that are from the same club')

    def delete_trainer(self, trainer_id: str) -> None:
        user = self.user_service.get_user_by_id(trainer_id)
        if user['club_ids'][0] == current_user['club_ids'][0] and user['role'] == 2:
            self.user_service.delete_user(trainer_id)
        else:
            raise Exception('Club admin can only delete trainers that are from the same club')

    def add_player(self, team_id: str, player_id: str) -> None:
        self.__get_connection()\
            .update_one({'_id': ObjectId(team_id)}, {'$addToSet': {'player_ids': ObjectId(player_id)}})

    def __get_connection(self) -> Collection:
        return self.connection_service.get_connection_by_club_id(ObjectId(current_user['club_ids'][0])).db.team

    def update_predictions(self, team_id):
        return {}
