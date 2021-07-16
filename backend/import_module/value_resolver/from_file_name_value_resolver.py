import os
import re

import pandas as pd

from import_module.model.file_import_configuration import FileImportConfiguration
from import_module.value_resolver.base_value_resolver import BaseValueResolver

"""
Requires:
    inner_name
    outer_identifier
    use_index=true
    separator 

Resolves value from file name using provided separator and index in separated array. 
Assigns same value for all records of the file as “inner_name”.
"""


class FromFileNameValueResolver(BaseValueResolver):
    def resolve_value(self, filename: str, df: pd.DataFrame, field_configuration: dict, result_df: pd.DataFrame):
        if not field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_USE_INDEX):
            raise Exception("FromFileNameValueResolver only supports indexed identifiers")
        _filename = os.path.splitext(filename)[0]
        if isinstance(field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER), list):
            split_file_name = _filename.split(field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_SEPARATOR))
            value = ' '.join([split_file_name[index] for index in field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)])
        else:
            value = _filename.split(field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_SEPARATOR))[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)]
            value = re.sub('[^A-Za-z]+', ' ', value)
        result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_INNER_NAME)] = value
