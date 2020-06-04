import os
import requests
import tempfile

from pandas import read_csv, to_datetime


def download_data_from_web(url):
    """
    Function for downloading data from specified URL.
    Data is saved to temporary directory (depending on OS)

    :param url: URL that points to data
    :type url: str

    :return: Path to temporary file with downladed data
    :rtype: str
    """
    web_data = requests.get(url)
    content = web_data.content.decode('utf-8').replace("\\r\\n", os.linesep)
    _, tmp_path = tempfile.mkstemp()
    with open(tmp_path, 'w') as f:
        f.write(content)
    return tmp_path


def create_data_frame(source, web=False):
    """
    Function for creating data frame from web or local data

    :param source: URL or filepath of data
    :type source: str
    :param web: Flag to indicate whether data should be downlaoded from the web
    :type web: bool

    :return: Parsed Pandas data frame
    :rtype: pandas.core.frame.DataFrame
    """
    if web:
        source = download_data_from_web(source)
    data = read_csv(source, lineterminator=os.linesep)
    data["Timestamp"] = to_datetime(data["Timestamp"], format="%d-%m-%Y")
    data["Sick"] = data["Confirmed"] - data["Deaths"] - data["Recovered"]
    data['D2D-deaths'] = data['Deaths'] - data['Deaths'].shift(1, fill_value=0)
    return data
