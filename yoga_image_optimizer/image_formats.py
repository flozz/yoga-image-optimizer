"""
Supported image formats.

::

    "<format_id>": {             # Internal ID for the format
        "display_name: str,      # The name of the format as displayed in the UI
        "exts": [".ext"],        # Possible file extentions for the format (lowercase)
        "mimetype": str,         # Mimetype (e.g. "image/jpeg")
        "input": bool,           # Is the format supported as input
        "output": bool,          # Is the format supported as output
        "check_function": None,  # | A fonction to check if a file is in the given format
                                 # | Check function definition: "def check(format_id, filename)"
    },
"""

import pathlib


IMAGES_FORMATS = {
    "jpeg": {
        "display_name": "JPEG",
        "exts": [".jpg", ".jpeg"],
        "mimetype": "image/jpeg",
        "input": True,
        "output": True,
        "check_function": "_check_extention",
    },
    "png": {
        "display_name": "PNG",
        "exts": [".png"],
        "mimetype": "image/png",
        "input": True,
        "output": True,
        "check_function": "_check_extention",
    },
}


def _check_extention(format_id, filename):
    """Check if the given file name matches the format extension.

    :param str format_id: The internal format identifier to check.
    :param str filename: The path of the file to check.

    :rtype: bool
    :return: whether or not the file name matches the format extensions.

    >>> _check_extention("jpeg", "test.jpg")
    True
    >>> _check_extention("jpeg", "test.jpeg")
    True
    >>> _check_extention("jpeg", "test.JPEG")
    True
    >>> _check_extention("png", "test.png")
    True
    >>> _check_extention("png", "test.jpg")
    False
    """
    exts = IMAGES_FORMATS[format_id]["exts"]
    return pathlib.Path(filename).suffix.lower() in exts


def find_file_format(filename):
    """Finds the format of the given file.

    :param str filename: The path of the file.

    :rtype: str or None
    :return: The format_id for the given file name or ``None``.

    >>> find_file_format("test.jpeg")
    'jpeg'
    >>> find_file_format("test.png")
    'png'
    >>> find_file_format("test.foo")
    """
    for format_id in IMAGES_FORMATS:
        checker_function = globals()[
            IMAGES_FORMATS[format_id]["check_function"]
        ]
        if checker_function(format_id, filename):
            return format_id
    return None


def get_supported_input_format_mimetypes():
    return [fmt["mimetype"] for fmt in IMAGES_FORMATS.values() if fmt["input"]]


def get_supported_output_format_ids():
    return [fid for fid, fmt in IMAGES_FORMATS.items() if fmt["output"]]


def get_supported_output_format_names():
    return [
        fmt["display_name"] for fmt in IMAGES_FORMATS.values() if fmt["output"]
    ]
