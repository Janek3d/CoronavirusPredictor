from data_gather.data_gather import create_data_frame


class CovidEstimator:

    def __init__(self, data=None):
        self._data = data

    def load_data(self, source, web=False):
        self._data = create_data_frame(source, web)

    @property
    def data(self):
        return self._data
