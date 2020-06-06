import dash
from datetime import datetime
import unittest

from callbacks.callbacks import CovidEstimator


class TestCovidEstimator(unittest.TestCase):

    def test_MA_model(self):
        c = CovidEstimator()
        c.load_data("https://raw.githubusercontent.com/dtandev/coronavirus/master/data/CoronavirusPL%20-%20General.csv", web=True)
        hmin = datetime(2020, 5, 20)
        hmax = datetime(2020, 7, 20)
        c.set_predict_horizon(hmin, hmax)
        c.train_MA()
        c.predict()
        self.assertIsInstance(type(c.get_dcc_Graph()),
                              dash.development.base_component.ComponentMeta)

    def test_AR_model(self):
        c = CovidEstimator()
        c.load_data("https://raw.githubusercontent.com/dtandev/coronavirus/master/data/CoronavirusPL%20-%20General.csv", web=True)
        hmin = datetime(2020, 5, 20)
        hmax = datetime(2020, 7, 20)
        c.set_predict_horizon(hmin, hmax)
        c.train_AR()
        c.predict()
        self.assertIsInstance(type(c.get_dcc_Graph()),
                              dash.development.base_component.ComponentMeta)
