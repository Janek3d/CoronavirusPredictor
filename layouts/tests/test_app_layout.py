import dash
import unittest

from layouts.app_layout import main_layout


class TestMainLayout(unittest.TestCase):

    def test_main_layout_content(self):
        self.assertIsInstance(type(main_layout()),
                              dash.development.base_component.ComponentMeta)
