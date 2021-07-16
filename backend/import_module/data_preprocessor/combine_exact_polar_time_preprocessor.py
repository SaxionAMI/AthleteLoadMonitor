from datetime import datetime

import pandas as pd

from import_module.data_preprocessor.base_preprocessor import BasePreprocessor
from import_module.model.file_import_configuration import FileImportConfiguration


class CombineExactPolarTimePreprocessor(BasePreprocessor):
    def execute(self, df: pd.DataFrame, filename: str, import_preprocessor: dict):
        df[import_preprocessor.get(FileImportConfiguration.ATTR_PREPROCESSOR_ASSIGN_TO_COLUMN)] = \
            pd.to_timedelta(df[import_preprocessor.get(FileImportConfiguration.ATTR_FIELD_VALUE_OUTER_IDENTIFIER)]) \
            + self.__get_time_from_filename(filename)

    def __get_time_from_filename(self, filename):
        date = datetime.date(datetime.strptime(filename.split('_')[0], '%Y%m%d'))
        time = datetime.time(datetime.strptime(filename.split('_')[1], '%H%M%S'))
        return datetime.combine(date, time)
