class FileImportConfiguration:
    ATTR_FIELD_VALUE_RESOLVER = 'value_resolver'
    ATTR_FIELD_VALUE_FROM_BODY = 'from_body'
    ATTR_FIELD_VALUE_USE_INDEX = 'use_index'
    ATTR_FIELD_VALUE_OUTER_IDENTIFIER = 'outer_identifier'
    ATTR_FIELD_VALUE_INNER_NAME = 'inner_name'
    ATTR_FIELD_VALUE_SEPARATOR = 'separator'
    ATTR_FIELD_VALUE_DATAFRAME_QUERY = 'dataframe_query'

    ATTR_PREPROCESSOR = 'preprocessor'
    ATTR_PREPROCESSOR_METHOD_VALUE = 'method_value'
    ATTR_PREPROCESSOR_ASSIGN_TO_COLUMN = 'assign_to_column'

    ATTR_MAPPING_FIELD_TOLERANCE_S = 'tolerance_s'
    ATTR_MAPPING_FIELD_NAME = 'field_name'

    def __init__(self, _id=None, name=None, extension=None, preprocessors=None, fields=None,
                 mapping_fields=None, create_new_if_not_mapped=None):
        if mapping_fields is None:
            mapping_fields = []
        if fields is None:
            fields = []
        if preprocessors is None:
            preprocessors = []
        self.value = {'_id': _id, 'name': name, 'extension': extension, 'preprocessors': preprocessors,
                      'fields': fields, 'mapping_fields': mapping_fields,
                      'create_new_if_not_mapped': create_new_if_not_mapped}

    @classmethod
    def from_dict(cls, input_dict: dict):
        return cls(input_dict.get('_id'), input_dict.get('name'), input_dict.get('extension'),
                   input_dict.get('preprocessors'), input_dict.get('fields'), input_dict.get('mapping_fields'),
                   input_dict.get('create_new_if_not_mapped'))

    def get_dict_value(self) -> dict:
        return {k: v for k, v in self.value.items() if v is not None}

    def get_id(self) -> str:
        return self.value['_id']

    def get_name(self) -> str:
        return self.value['name']

    def get_extension(self) -> str:
        return self.value['extension']

    def get_preprocessors(self) -> str:
        return self.value['preprocessors']

    def get_fields(self) -> str:
        return self.value['fields']

    def get_mapping_fields(self) -> str:
        return self.value['mapping_fields']

    def create_new_if_not_mapped(self) -> str:
        return self.value['create_new_if_not_mapped']
