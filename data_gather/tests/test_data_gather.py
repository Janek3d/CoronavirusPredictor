from mock import patch
import os
from parameterized import parameterized
from pyfakefs import fake_filesystem_unittest
from datetime import datetime

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
    "linux.test":
    "Timestamp,Confirmed,Deaths,Recovered,In_the_hospital,In_quarantine,Under_medical_supervision,Number_of_tests_carried_out\n03-03-2020,0,0,0,68,316,4459,559\n04-03-2020,1,0,0,65,349,4540,584\n05-03-2020,1,0,0,92,490,5647,676",
    "windows.test":
    "Timestamp,Confirmed,Deaths,Recovered,In_the_hospital,In_quarantine,Under_medical_supervision,Number_of_tests_carried_out\\r\\n03-03-2020,0,0,0,68,316,4459,559\\r\\n04-03-2020,1,0,0,65,349,4540,584\\r\\n05-03-2020,1,0,0,92,490,5647,676"
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

    expectedDF = DataFrame.from_dict({
        'Timestamp': {
            0: datetime(2020, 3, 3),
            1: datetime(2020, 3, 4),
            2: datetime(2020, 3, 5)
        },
        'Confirmed': {
            0: 0,
            1: 1,
            2: 1
        },
        'Deaths': {
            0: 0,
            1: 0,
            2: 0
        },
        'Recovered': {
            0: 0,
            1: 0,
            2: 0
        },
        'In_the_hospital': {
            0: 68,
            1: 65,
            2: 92
        },
        'In_quarantine': {
            0: 316,
            1: 349,
            2: 490
        },
        'Under_medical_supervision': {
            0: 4459,
            1: 4540,
            2: 5647
        },
        'Number_of_tests_carried_out': {
            0: 559,
            1: 584,
            2: 676
        },
        'Sick': {
            0: 0,
            1: 1,
            2: 1
        }
    })

    def SetUp(self):
        self.setUpPyfakefs()

    @parameterized.expand(list(mock_create_data.keys()))
    @patch('requests.get', side_effect=url_get_mock)
    def test_url_source_linux_formatting(self, url, mock_get):
        df = create_data_frame(url, web=True)
        print(df.to_dict())
        assert_frame_equal(df, self.expectedDF)

    def test_data_from_file(self):
        with open('testfile', 'w') as f:
            f.write(mock_create_data['linux.test'])
        df = create_data_frame('testfile')
        assert_frame_equal(df, self.expectedDF)
        os.remove('testfile')
