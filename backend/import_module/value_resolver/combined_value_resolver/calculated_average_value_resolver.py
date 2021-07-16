import pandas as pd

from import_module.model.file_import_configuration import FileImportConfiguration
from import_module.value_resolver.base_value_resolver import BaseValueResolver

"""
Requires:
    inner_name
    outer_identifier (array of two strings. 1st string - distance column, 2nd string - duration column)

Calculates average speed based on two “outer_identifiers” 
and converts it from m/s to km/h. Assigns value to “inner_name”.
"""


class CalculatedAverageValueResolver(BaseValueResolver):
    def resolve_value(self, filename: str, df: pd.DataFrame, field_configuration: dict, result_df: pd.DataFrame):
        value = round(3.6 * result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)[0]].iloc[-1] /
                      result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)[1]].iloc[-1], 1)
        result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_INNER_NAME)] = value
