from mock import patch
from parameterized import parameterized
from pyfakefs import fake_filesystem_unittest

from requests.exceptions import MissingSchema
from pandas.util.testing import assert_frame_equal
from pandas import DataFrame

from ..data_gather import create_data_frame, download_data_from_web

mock_data_url = {
    "data1.test": "data1content",
    "data2.test": "data2content",
    "data3.test": "data3content",
}

mock_create_data = {
    "linux.test": "a,b,c\n1,veni,0.9\n2,vidi,0.8\n3,vici,0.7",
    'windows.test': "a,b,c\\r\\n1,veni,0.9\\r\\n2,vidi,0.8\\r\\n3,vici,0.7"
}


class MockRequestReturn:
    def __init__(self, content=""):
        self.content = content.encode('utf-8')


def url_get_mock(url):
    if url in mock_data_url.keys():
        return MockRequestReturn(mock_data_url[url])
    elif url in mock_create_data.keys():
        return MockRequestReturn(mock_create_data[url])
    else:
        raise MissingSchema('Invalid URL')


class TestDownloadDataFromWeb(fake_filesystem_unittest.TestCase):

    def SetUp(self):
        self.setUpPyfakefs()

    @parameterized.expand(list(mock_data_url.items()))
    @patch('requests.get', side_effect=url_get_mock)
    def test_download_proper_data(self, url, expected_data, mock_get):
        tmp_file = download_data_from_web(url)
        with open(tmp_file, 'r') as f:
            self.assertEqual(f.read(), expected_data)

    @patch('requests.get', side_effect=url_get_mock)
    def test_invalid_url(self, mock_get):
        with self.assertRaises(MissingSchema) as _:
            download_data_from_web('invalid.url')


class TestCreateDataFrame(fake_filesystem_unittest.TestCase):

    expectedDF = DataFrame(data={
        'a': [1, 2, 3],
        'b': ['veni', 'vidi', 'vici'],
        'c': [0.9, 0.8, 0.7]
    })

    def SetUp(self):
        self.setUpPyfakefs()

    @parameterized.expand(list(mock_create_data.keys()))
    @patch('requests.get', side_effect=url_get_mock)
    def test_url_source_linux_formatting(self, url, mock_get):
        df = create_data_frame(url, web=True)
        assert_frame_equal(df, self.expectedDF)

    def test_data_from_file(self):
        with open('testfile', 'w') as f:
            f.write(mock_create_data['linux.test'])
        df = create_data_frame('testfile')
        assert_frame_equal(df, self.expectedDF)
