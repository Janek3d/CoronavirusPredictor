import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima_model import ARMA

from data_gather.data_gather import create_data_frame


class CovidEstimator:
    """This class supports setup, training and prediction of two selected alogrithms.
    """
    def __init__(self, data=None):
        """Provided data should be properly formatted data frame
        with data format provided as by github.com/dtandev/coronavirus

        :param data: DataFrame with data
        :type data: pandas.core.frame.DataFrame
        """
        self._data = data

    def set_predict_horizon(self, horizon):
        """Set predict horizon to which estimator should predict newxt data points

        :param horizon: specific data in the future (should be greater than max data date)
        :type horizon: datetime.datetime
        """
        data_max = max(self._data["Timestamp"])
        if horizon < data_max:
            raise Exception("Predict horizon may not be lower than data")
        time_delta = horizon - data_max
        self._horizon = self._data.sort_values(
            by="Timestamp")["Timestamp"].values[-1] + pd.to_timedelta(
                np.arange(time_delta.days + 1), 'D')

    def load_data(self, source, web=False):
        """Loads data from file or web
        :param source: Path or url to data
        :type source: str
        :param web: Flag to indicate whether data should be downloaded from the web
        :type web: bool
        """
        self._data = create_data_frame(source, web)

    def train_AR(self):
        """Train Autoregression model with data
        """
        if len(self._data) < 3:
            raise Exception('Please provide data with more points')
        model = AutoReg(self._data["Sick"], lags=int(len(self._data) / 3))
        self._model = model.fit()

    def train_MA(self):
        """Train Autoregressive Integrated Moving Average
        """
        if len(self._data) < 3:
            raise Exception('Please provide data with more points')
        model = ARMA(self._data["Sick"], order=(3, 2))
        self._model = model.fit()

    def predict(self):
        """Predict next data points based on set horizon and created model
        In order to run predict please first run set_predict_horizon() and train_*() function.
        """
        if self._horizon is not None and self._model is not None:
            self._predicted_data = self._model.predict(
                len(self._data),
                len(self._data) + len(self._horizon))[2:]
            self._predicted_data = pd.concat([
                pd.Series(
                    self._data.sort_values(by="Timestamp")["Sick"].values[-1]),
                self._predicted_data
            ])
        else:
            raise Exception('No horizon is set or model is not trained')

    def plt(self):
        """Plot simple matplotlib figure with data and predicted points
        Should be used after predict() function has been run successfully
        """
        _, ax1 = plt.subplots(1)
        ax1.plot(self._horizon, self._predicted_data)
        self._data.plot(x="Timestamp", y="Sick", ax=ax1)
        plt.grid()
        plt.show()

    @property
    def data(self):
        """Return class data
        :return: Class data
        :rtype: pandas.core.frame.DataFrame
        """
        return self._data
