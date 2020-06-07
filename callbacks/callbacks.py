import dash_core_components as dcc
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.var_model import VARResultsWrapper

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
        self._horizon_min = datetime(2020, 3, 3)

    def invert_transformation(self, df_train, df_forecast, second_diff=False):
        """Revert back the differencing to get the forecast to original scale."""
        df_fc = df_forecast.copy()
        columns = df_train.columns
        for col in columns:        
            # Roll back 2nd Diff
            if second_diff:
                df_fc[str(col)+'_1d'] = (df_train[col].iloc[-1]-df_train[col].iloc[-2]) + df_fc[str(col)+'_2d'].cumsum()
            # Roll back 1st Diff
            df_fc[str(col)+'_forecast'] = df_train[col].iloc[-1] + df_fc[str(col)+'_1d'].cumsum()
        return df_fc

    def set_predict_horizon(self, horizon_min, horizon_max):
        """Set predict horizon to which estimator should predict newxt data points

        :param horizon_min: Start date of prediction
        :type horizon_min: datetime.datetime
        :param horizon_max: Stop date of prediction
        :type horizon_max: datetime.datetime
        """
        if horizon_max < horizon_min:
            raise Exception("Max horizon date may not me lower than min horizon date")
        data_max = max(self._data["Timestamp"])
        if horizon_min > data_max:
            raise Exception("Prediction may not start after end of actual data")
        self._horizon_min = horizon_min
        time_delta = horizon_max - horizon_min
        self._horizon = horizon_min + pd.to_timedelta(
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
        model = AutoReg(self._data["Deaths"], lags=int(len(self._data) / 3))
        self._model = model.fit()

    def train_MA(self):
        """Train Autoregressive Integrated Moving Average
        """
        if len(self._data) < 3:
            raise Exception('Please provide data with more points')
        model = ARMA(self._data["Deaths"], order=(1, 0))
        self._model = model.fit()

    def train_VAR(self):
        data_diff = self._data.diff().dropna()
        self._data_diff2 = data_diff.diff().dropna()
        model = VAR(self._data_diff2[['Confirmed','Deaths','Recovered']])
        self._model = model.fit(maxlags=15, ic='aic')

    def predict(self):
        """Predict next data points based on set horizon and created model
        In order to run predict please first run set_predict_horizon() and train_*() function.
        """
        if isinstance(self._model, VARResultsWrapper):
            predicted_data = self._model.forecast(self._data_diff2[[
                'Confirmed','Deaths','Recovered']].values[-len(self._horizon)+1:], len(self._horizon))
            pred_diff = pd.DataFrame(predicted_data, columns=['Confirmed','Deaths','Recovered'])
            pred_diff.columns+='_2d'
            X_train =  self._data[[
                'Confirmed','Deaths','Recovered']][0:-len(self._horizon)]
            df_result = self.invert_transformation(X_train,pred_diff,second_diff=True)
            df_result['D2D-deaths'] = df_result['Deaths_forecast']-df_result['Deaths_forecast'].shift(1,fill_value=0)
            self._predicted_data = df_result['D2D-deaths']
            self._predicted_data = pd.concat([
                pd.Series(
                    self._data.loc[self._data['Timestamp']==self._horizon_min]["D2D-deaths"]),
                self._predicted_data
            ])

        elif self._horizon is not None and self._model is not None:
            self._predicted_data = self._model.predict(
                len(self._data),
                len(self._data) + len(self._horizon))
            self._predicted_data = (self._predicted_data - self._predicted_data.shift(1, fill_value=0))[2:]
            self._predicted_data = pd.concat([
                pd.Series(
                    self._data.loc[self._data['Timestamp']==self._horizon_min]["D2D-deaths"]),
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
        self._data.plot(x="Timestamp", y="D2D-deaths", ax=ax1)
        plt.grid()
        plt.show()

    def get_dcc_Graph(self):
        """Returns dash core component Graph with predicted data

        :return: Dash Core Component Graph with data and predictions
        :rtype: dash_core_components.Graph.Graph
        """
        return dcc.Graph(
            figure=dict(
                data=[
                    dict(
                        x=list(self._data["Timestamp"]),
                        y=list(self._data["D2D-deaths"]),
                        name='Historical data',
                        marker=dict(
                          color='rgb(55, 83, 109)'
                        )
                    ),
                    dict(
                        x=self._horizon,
                        y=self._predicted_data,
                        name='Prediction',
                        marker=dict(
                            color='rgb(26, 118, 255)'
                            )
                        )
                    ],
                layout=dict(
                    title='COVID-19 day to day deaths People Prediction',
                    showlegend=True,
                    legend=dict(
                        x=0,
                        y=1.0
                    ),
                    margin=dict(l=40, r=0, t=40, b=30)
                )
            ),
            id='graph'
        )

    @property
    def data(self):
        """Return class data
        :return: Class data
        :rtype: pandas.core.frame.DataFrame
        """
        return self._data

    @property
    def model(self):
        """Return class trained model
        :return: Class model
        :rtype: statsmodels.tsa.arima.ARIMAResults
        """
        return self._model
