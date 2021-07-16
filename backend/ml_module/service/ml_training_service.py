import os
from typing import List

import pandas as pd
from bson import ObjectId
from flask_jwt_extended import current_user

from ml_module.common.generic_data_analyzer import Analyzer
from ml_module.model.ml_configuration import MLConfiguration
from service.connection_service import ConnectionService
import pickle


class MLTrainingService:
    def __init__(self, connection_service: ConnectionService):
        self.connection_service = connection_service

    def train_new_model(self, start_date, end_date):
        ml_configuration_list = self.__get_ml_configuration()
        for ml_configuration in ml_configuration_list:
            if len(ml_configuration.get_training_fields()) == 0:
                continue
            records = self.__get_trainings_in_range(start_date, end_date)
            df = pd.DataFrame(list(records))
            analyzer = Analyzer(df)
            analyzer.set_inputs(ml_configuration.get_training_fields())
            analyzer.set_outputs(ml_configuration.get_training_label_field())
            analyzer.train_model()
            self.__save_analyzer(analyzer, ml_configuration.get_predicted_value_name())
            self.update_specific_predictions(ml_configuration.get_predicted_value_name())

    def update_specific_predictions(self, name: str):
        if not os.path.exists(f"analyzers/{current_user['club_ids'][0]}/{name}.pkl"):
            raise Exception(f'Analyzer is not trained for {name} feature')

        trainings = self.__get_connection_db().training.find({})
        df = pd.DataFrame(trainings)

        with open(f"analyzers/{current_user['club_ids'][0]}/{name}.pkl", 'rb') as f:
            analyzer = pickle.load(f)
            predictions, _, _ = analyzer.predict(df)
            df[name] = predictions
            for row in df.itertuples():
                self.__get_connection_db().training.update_one({'_id': getattr(row, '_1')}, {'$set': {name: getattr(row, name)}})

    def __save_analyzer(self, model, name):
        if not os.path.exists(f"analyzers/{current_user['club_ids'][0]}"):
            os.makedirs(f"analyzers/{current_user['club_ids'][0]}")
        with open(f"analyzers/{current_user['club_ids'][0]}/{name}.pkl", 'wb') as f:
            pickle.dump(model, f)

    def __get_ml_configuration(self) -> List[MLConfiguration]:
        return [MLConfiguration.from_dict(v) for v in self.__get_connection_db().ml_configuration.find()]

    def __get_trainings_in_range(self, start_date, end_date):
        query = {}
        if start_date is not None and end_date is not None:
            query = {'timestamp': {'$gte': start_date, '$lt': end_date}}
        elif start_date is not None:
            query = {'timestamp': {'$gte': start_date}}
        elif end_date is not None:
            query = {'timestamp': {'$lt': end_date}}
        return self.__get_connection_db().training.find(query)


    def __get_connection_db(self):
        return self.connection_service.get_connection_by_club_id(ObjectId(current_user['club_ids'][0])).db
