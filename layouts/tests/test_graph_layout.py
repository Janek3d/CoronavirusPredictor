import dash
import unittest

from ..graph_layout import graph_layout


class TestMainLayout(unittest.TestCase):

    def test_graph_layout_content(self):
        self.assertIsInstance(type(graph_layout()),
                              dash.development.base_component.ComponentMeta)
