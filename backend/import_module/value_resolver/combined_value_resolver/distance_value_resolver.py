import pandas as pd

from import_module.model.file_import_configuration import FileImportConfiguration
from import_module.value_resolver.base_value_resolver import BaseValueResolver

"""
Requires:
    inner_name
    outer_identifier
    dataframe_query

Calculates distance value (from column “outer_identifier”) 
of specific speed (specified in dataframe query). Assigns value to “inner_name”.

"""


class DistanceValueResolver(BaseValueResolver):
    def resolve_value(self, filename: str, df: pd.DataFrame, field_configuration: dict, result_df: pd.DataFrame):
        filtered_df = df.query(self.resolve_dataframe_filter(field_configuration))
        if len(filtered_df) > 0:
            result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_INNER_NAME)] = \
                round(filtered_df[
                          field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)].sum(), 1)
        else:
            result_df[field_configuration.get(FileImportConfiguration.ATTR_FIELD_VALUE_INNER_NAME)] = 0
