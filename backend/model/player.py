from typing import Optional, List

from model.base import Base


class Player(Base):
    def __init__(self, _id=None, image_url=None, name=None, position=None, name_variations=None,
                 risk=None, latest_training=None):
        super().__init__(_id, image_url)
        self.value['name'] = name
        self.value['position'] = position
        self.value['name_variations'] = name_variations
        self.value['risk'] = risk
        self.value['latest_training'] = latest_training

    @classmethod
    def from_dict(cls, input_dict):
        return cls(_id=input_dict['_id'],
                   image_url=input_dict['image_url'],
                   name=input_dict['name'],
                   position=input_dict['position'],
                   name_variations=input_dict['name_variations'])

    def get_name(self) -> str:
        return self.value['name']

    def get_position(self) -> str:
        return self.value['position']

    def get_name_variations(self) -> List[str]:
        return self.value['name_variations']

    def get_risk(self) -> str:
        return self.value['risk']

    def get_latest_training(self) -> int:
        return self.value['latest_training']

    def set_name(self, name: Optional[str]):
        self.value['name'] = name

    def set_position(self, position: Optional[str]):
        self.value['position'] = position

    def set_name_variations(self, variations: List[str]):
        self.value['name_variations'] = variations

    def set_risk(self, risk: Optional[str]):
        self.value['risk'] = risk

    def set_latest_training(self, latest_training: Optional[int]):
        self.value['latest_training'] = latest_training
