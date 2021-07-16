from abc import ABC, abstractmethod

import pandas as pd


class BasePreprocessor(ABC):

    @abstractmethod
    def execute(self, df: pd.DataFrame, filename: str, import_preprocessor: dict):
        pass
