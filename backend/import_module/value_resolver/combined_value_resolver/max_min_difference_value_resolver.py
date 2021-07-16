import pandas as pd

from import_module.model.file_import_configuration import FileImportConfiguration
from import_module.value_resolver.base_value_resolver import BaseValueResolver

"""
Requires:
    inner_name
    outer_identifier

Calculates delta of the largest and smallest value in the column (outer_identifier)
"""


class MaxMinDifferenceValueResolver(BaseValueResolver):
    def resolve_value(self, filename: str, df: pd.DataFrame, field_configuration: dict, result_df: pd.DataFrame):
        value = (df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)].max()
                 - df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)].min())
        if isinstance(value, pd.Timedelta):
            value = value.seconds
        result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_INNER_NAME)] = [value]
