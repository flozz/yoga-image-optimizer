from pathlib import Path


def find_data_path(path):
    path_file = Path(__file__)
    root = path_file.parent.resolve()
    return root.joinpath("data", path).as_posix()
