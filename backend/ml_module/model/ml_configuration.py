from typing import List


class MLConfiguration:
    def __init__(self, _id=None, predicted_value_name=None, training_fields=None, training_label_field=None,
                 display_label=None, avg_field=None):
        if training_fields is None:
            training_fields = []
        self.value = {'_id': _id, 'predicted_value_name': predicted_value_name, 'training_fields': training_fields,
                      'training_label_field': training_label_field, 'display_label': display_label,
                      'avg_field': avg_field}

    @classmethod
    def from_dict(cls, input_dict: dict):
        return cls(input_dict.get('_id'), input_dict.get('predicted_value_name'), input_dict.get('training_fields'),
                   input_dict.get('training_label_field'), input_dict.get('display_label'), input_dict.get('avg_field'))

    def get_dict_value(self) -> dict:
        return {k: v for k, v in self.value.items() if v is not None}

    def get_id(self) -> str:
        return self.value['_id']

    def get_predicted_value_name(self) -> str:
        return self.value['predicted_value_name']

    def get_training_fields(self) -> List[str]:
        return self.value['training_fields']

    def get_training_label_field(self) -> str:
        return self.value['training_label_field']

    def get_display_label(self) -> str:
        return self.value['display_label']

    def get_avg_field(self) -> str:
        return self.value['avg_field']
