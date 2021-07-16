import pandas as pd

from import_module.model.file_import_configuration import FileImportConfiguration
from import_module.value_resolver.base_value_resolver import BaseValueResolver

"""
Requires:
    inner_name
    outer_identifier

Resolves array of datetime values from specified “outer_identifier” column and 
assigns values to result record as “inner_name”.
"""


class TimestampBodyResolver(BaseValueResolver):
    def resolve_value(self, filename: str, df: pd.DataFrame, field_configuration: dict, result_df: pd.DataFrame):
        result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_INNER_NAME)] \
            = pd.to_datetime(df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)])
