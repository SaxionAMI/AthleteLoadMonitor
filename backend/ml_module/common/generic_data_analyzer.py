from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.impute import SimpleImputer
import pandas as pd

class Analyzer():

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.inputs = []
        self.output = []
        self.__train_features = None
        self.__labels = None
        self.__model = None

    def set_inputs(self, inputs):
        self.inputs = inputs

    def set_outputs(self, output):
        self.output = output

    def train_model(self):
        if not self.inputs:
            raise Exception('no inputs set')
        if not self.output:
            raise Exception('no output set')

        df = self.data
        df = df.dropna()  # drop incomplete data

        self.__train_features = df[self.inputs]
        self.__labels = df[[self.output]].values.ravel()

        vot_reg = VotingRegressor([('svr', SVR()), ('ridge', Ridge())])

        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('algorithm', vot_reg)
        ])

        pipe.fit(self.__train_features, self.__labels)
        self.__model = pipe

    def predict(self, df=None):
        """
        Predict values of dataframe, using set inputs. Predictions are imputed (missing values
        replaced by mean value); performance metrices are derived from part without missing
        values.
        :param df: DataFrame to perform predictions on
        :return: predictions (np.array), RMSE, MAE
        """
        if df is None:
            raise Exception("Dataframe is required")
        # determine predictions for entire dataframe. Impute missing values
        features = df[self.inputs]
        imp_mean = SimpleImputer(strategy='mean')
        features = imp_mean.fit_transform(features)
        predictions = self.__model.predict(features)

        # for performance metrics no nans are allowed
        df = df.dropna(subset=[self.output])
        features = df[self.inputs]
        labels = df[[self.output]].values.ravel()
        imp_mean = SimpleImputer(strategy='mean')
        features = imp_mean.fit_transform(features)
        preds = self.__model.predict(features)

        mae = mean_absolute_error(labels, preds)
        rmse = mean_squared_error(labels, preds, squared=False)

        return predictions, rmse, mae
