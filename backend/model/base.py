from abc import ABC, abstractmethod
from typing import Optional


class Base(ABC):

    def __init__(self, _id=None, image_url=None):
        self.value = {'_id': _id, 'image_url': image_url}

    @classmethod
    @abstractmethod
    def from_dict(cls, input_dict):
        pass

    def get_dict_value(self) -> dict:
        return {k: v for k, v in self.value.items() if v is not None}

    def get_id(self) -> str:
        return self.value['_id']

    def get_image_url(self) -> str:
        return self.value['image_url']

    def set_id(self, _id: Optional[str]):
        self.value['_id'] = _id

    def set_image_url(self, image_name: Optional[str]):
        self.value['image_url'] = image_name
