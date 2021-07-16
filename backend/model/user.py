from typing import List, Optional

from bson import ObjectId

from model.base import Base


class User(Base):
    def __init__(self, _id=None, image_url=None, email=None, password=None, role=None, team_ids=None, club_ids=None):
        super().__init__(_id, image_url)
        self.value['email'] = email
        self.value['password'] = password
        self.value['role'] = role
        self.value['team_ids'] = team_ids
        self.value['club_ids'] = club_ids

    @classmethod
    def from_dict(cls, input_dict):
        return cls(_id=input_dict.get('_id'),
                   image_url=input_dict.get('image_url'),
                   email=input_dict.get('email'),
                   password=input_dict.get('password'),
                   role=input_dict.get('role'),
                   team_ids=input_dict.get('team_ids'),
                   club_ids=input_dict.get('club_ids'))

    def get_email(self) -> str:
        return self.value['email']

    def get_password(self) -> str:
        return self.value['password']

    def get_role(self) -> int:
        return self.value['role']

    def get_team_ids(self) -> List[ObjectId]:
        return self.value['team_ids']

    def get_club_ids(self) -> List[ObjectId]:
        return self.value['club_ids']

    def set_password(self, password: Optional[str]):
        self.value['password'] = password

    def set_team_ids(self, team_ids: Optional[List[ObjectId]]):
        self.value['team_ids'] = team_ids

    def set_club_ids(self, club_ids: Optional[List[ObjectId]]):
        self.value['club_ids'] = club_ids


