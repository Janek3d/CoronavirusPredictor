import dash
import unittest

from ..app_layout import upload_data_layout, predict_horizon_layout, \
                         main_layout


class TestUploadDataLayout(unittest.TestCase):

    def test_upload_data_layout_content(self):
        self.assertIsInstance(type(upload_data_layout()),
                              dash.development.base_component.ComponentMeta)


class TestPredictHorizonLayout(unittest.TestCase):

    def test_predict_horizon_layout_content(self):
        self.assertIsInstance(type(predict_horizon_layout()),
                              dash.development.base_component.ComponentMeta)


class TestMainLayout(unittest.TestCase):

    def test_main_layout_content(self):
        self.assertIsInstance(type(main_layout()),
                              dash.development.base_component.ComponentMeta)
