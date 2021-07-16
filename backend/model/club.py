from typing import Optional

from model.base import Base


class Club(Base):
    def __init__(self, _id=None, image_url=None, name=None, database_url=None):
        super().__init__(_id, image_url)
        self.value['name'] = name
        self.value['database_url'] = database_url

    @classmethod
    def from_dict(cls, input_dict):
        return cls(_id=input_dict.get('_id'),
                   image_url=input_dict.get('image_url'),
                   name=input_dict.get('name'),
                   database_url=input_dict.get('database_url'))

    def get_name(self) -> str:
        return self.value['name']

    def get_database_url(self) -> str:
        return self.value['database_url']

    def set_name(self, name: Optional[str]):
        self.value['name'] = name

    def set_database_url(self, database_url: Optional[str]):
        self.value['database_url'] = database_url
