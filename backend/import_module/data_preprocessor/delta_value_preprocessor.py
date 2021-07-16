import pandas as pd

from import_module.data_preprocessor.base_preprocessor import BasePreprocessor
from import_module.model.file_import_configuration import FileImportConfiguration


class DeltaValuePreprocessor(BasePreprocessor):
    def execute(self, df: pd.DataFrame, filename: str, import_preprocessor: dict):
        df[import_preprocessor.get(FileImportConfiguration.ATTR_PREPROCESSOR_ASSIGN_TO_COLUMN)] = \
            df[import_preprocessor.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)] \
            - df[import_preprocessor.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)]\
                .shift(import_preprocessor.get(FileImportConfiguration.ATTR_PREPROCESSOR_METHOD_VALUE)).fillna(0)
