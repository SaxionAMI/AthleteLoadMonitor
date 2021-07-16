import numpy as np
import pandas as pd

from import_module.model.file_import_configuration import FileImportConfiguration
from import_module.value_resolver.base_value_resolver import BaseValueResolver

"""
Requires:
    inner_name
    dataframe_query

Calculates how many continuous actions are in the file 
based on the “dataframe_query”. Assigns value to “inner_name”.
"""


class ActionCountResolver(BaseValueResolver):
    def resolve_value(self, filename: str, df: pd.DataFrame, field_configuration: dict, result_df: pd.DataFrame):
        df_filter = self.resolve_dataframe_filter(field_configuration)
        df.loc[df.eval(df_filter), 'speed_cond'] = 1
        df.loc[~df.eval(df_filter), 'speed_cond'] = 0
        diff = df['speed_cond'] - df['speed_cond'].shift(1)
        result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_INNER_NAME)] \
            = int(np.nansum(diff[diff > 0]))
