import numpy as np
import pandas as pd

from import_module.model.file_import_configuration import FileImportConfiguration
from import_module.value_resolver.base_value_resolver import BaseValueResolver

"""
Requires:
    inner_name
    outer_identifier
    dataframe_query

Calculates specific heart rate zone based on dataframe_query. 
Assigns value to “inner_name”.
"""


class HrZoneValueResolver(BaseValueResolver):
    def resolve_value(self, filename: str, df: pd.DataFrame, field_configuration: dict, result_df: pd.DataFrame):
        filtered_df = df.query(self.resolve_dataframe_filter(field_configuration))
        if len(filtered_df) > 0:
            time = (df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)].max()
                    - df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)].min()).seconds
            result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_INNER_NAME)] = [np.round(100 * (len(filtered_df) / 10) / time, 2)]
        else:
            result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_INNER_NAME)] = [0]
