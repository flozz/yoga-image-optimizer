import os


def find_data_path(path):
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, "data", path)
