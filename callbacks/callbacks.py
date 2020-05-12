from data_gather.data_gather import create_data_frame


def load_data(source, web=False):
    data = create_data_frame(source, web)
    return data.info()
