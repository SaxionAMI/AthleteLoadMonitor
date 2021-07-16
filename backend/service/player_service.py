from typing import List

from bson import ObjectId
from flask_jwt_extended import current_user
from pymongo.collection import Collection

from model.player import Player
from model.team import Team
from service.connection_service import ConnectionService
from service.team_service import TeamService
from import_module.service.import_process_service import ImportProcessService


class PlayerService:
    def __init__(self, connection_service: ConnectionService, team_service: TeamService,
                 import_service: ImportProcessService):
        self.connection_service = connection_service
        self.team_service = team_service
        self.import_service = import_service

    def get_by_id(self, player_id: str) -> Player:
        return self.__get_connection().find_one({'_id': ObjectId(player_id)})

    def add(self, player: Player) -> str:
        if player.get_image_url() is None:
            player.set_image_url('defaultavatar.png')
        player_id = self.__get_connection().insert_one(player.get_dict_value()).inserted_id
        self.import_service.update_unmapped_player(player.get_name())
        return player_id

    def delete(self, player_id: str) -> None:
        self.__get_connection().delete_one({'_id': ObjectId(player_id)})

    def edit(self, player: Player) -> None:
        player_id = player.get_id()
        player.set_id(None)
        self.__get_connection().update_one({'_id': ObjectId(player_id)}, {'$set': player.get_dict_value()})

    def get_all(self) -> List[Player]:
        return [Player.from_dict(doc) for doc in self.__get_connection().find()]

    def get_team_all(self, team_id: str) -> List[Player]:
        team = self.team_service.get_team_by_id(team_id)
        if team is None:
            return []
        return [self.__add_additional_information_to_player(Player.from_dict(doc))
                for doc in self.__get_connection().find({'_id': {'$in': team.get_player_ids()}})]

    def change_team(self, old_team_id: str, new_team_id: str, player_id: str) -> None:
        old_team = self.team_service.get_team_by_id(old_team_id)
        new_team = self.team_service.get_team_by_id(new_team_id)

        if ObjectId(player_id) not in old_team.get_player_ids():
            raise AttributeError("Player is not in old_team")
        if ObjectId(player_id) in new_team.get_player_ids():
            raise AttributeError('Player is already in this team')
        old_team.get_player_ids().remove(ObjectId(player_id))
        new_team.get_player_ids().append(ObjectId(player_id))
        self.team_service.edit(Team(_id=old_team_id, player_ids=old_team.get_player_ids()))
        self.team_service.edit(Team(_id=new_team_id, player_ids=new_team.get_player_ids()))

    def add_name_variation(self, player_id, name):
        self.__get_connection().update_one({'_id': ObjectId(player_id)}, {'$addToSet': {'name_variations': name}})
        self.import_service.update_unmapped_player(name)

    def __add_additional_information_to_player(self, player: Player):
        latest_training_cursor = self.connection_service.get_connection_by_club_id(ObjectId(current_user['club_ids'][0]))\
            .db.training.find({'player_id': ObjectId(player.get_id())}).sort('timestamp', -1).limit(1)

        try:
            latest_training = latest_training_cursor.next()
        except StopIteration:
            return player

        actual = latest_training.get('rpe')
        predicted = latest_training.get('p_RPE')
        if actual is not None and predicted is not None:
            risk = 'low'
            if abs(predicted - actual) > 2.5:
                risk = 'high'
            elif abs(predicted - actual) > 1.5:
                risk = 'medium'
            player.set_risk(risk)
        player.set_latest_training(latest_training.get('timestamp'))
        return player


    def __get_connection(self) -> Collection:
        return self.connection_service.get_connection_by_club_id(ObjectId(current_user['club_ids'][0])).db.player
