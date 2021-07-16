from typing import Optional, List

from bson import ObjectId

from model.base import Base


class Team(Base):
    def __init__(self, _id=None, image_url=None, name=None, player_ids=None):
        super().__init__(_id, image_url)
        self.value['name'] = name
        self.value['player_ids'] = player_ids

    @classmethod
    def from_dict(cls, input_dict):
        return cls(_id=input_dict.get('_id'),
                   image_url=input_dict.get('image_url'),
                   name=input_dict.get('name'),
                   player_ids=input_dict.get('player_ids'))

    def get_name(self) -> str:
        return self.value['name']

    def get_player_ids(self) -> List[ObjectId]:
        return self.value['player_ids']

    def set_name(self, name: Optional[str]):
        self.value['name'] = name

    def set_player_ids(self, player_ids: Optional[List[ObjectId]]):
        self.value['player_ids'] = player_ids
