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
from .translation import gettext as _


IMAGES_FORMATS = {
    # ==== Formats supported as output ====
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
    "webp": {
        "display_name": "WebP",
        "exts": [".webp"],
        "mimetype": "image/webp",
        "input": True,
        "output": True,
        "check_function": "_check_extention",
    },
    "webpl": {
        "display_name": _("WebP (lossless)"),
        "exts": [".webp"],
        "mimetype": "image/webp",
        "input": True,
        "output": True,
        "check_function": "_check_nop",
    },
    # ==== Formats only supported as input ====
    "bmp": {
        "display_name": _("Windows Bitmap"),
        "exts": [".bmp", ".dib"],
        "mimetype": "image/bmp",
        "input": True,
        "output": False,
        "check_function": "_check_extention",
    },
    "eps": {
        "display_name": "EPS",
        "exts": [".eps"],
        "mimetype": "image/x-eps",
        "input": True,
        "output": False,
        "check_function": "_check_extention",
    },
    "gif": {
        "display_name": "GIF",
        "exts": [".gif"],
        "mimetype": "image/gif",
        "input": True,
        "output": False,
        "check_function": "_check_extention",
    },
    "icns": {
        "display_name": _("MacOS Icon (ICNS)"),
        "exts": [".icns"],
        "mimetype": "image/x-icns",
        "input": True,
        "output": False,
        "check_function": "_check_extention",
    },
    "ico": {
        "display_name": _("Windows Icon (ICO)"),
        "exts": [".ico"],
        "mimetype": "image/vnd.microsoft.icon",
        "input": True,
        "output": False,
        "check_function": "_check_extention",
    },
    "tga": {
        "display_name": "Truevision TGA",
        "exts": [".tga"],
        "mimetype": "image/x-tga",
        "input": True,
        "output": False,
        "check_function": "_check_extention",
    },
    "tiff": {
        "display_name": "TIFF",
        "exts": [".tiff", ".tif"],
        "mimetype": "image/tiff",
        "input": True,
        "output": False,
        "check_function": "_check_extention",
    },
    # ==== TODO ====
    # BLP
    # CUR
    # DCX
    # DDS
    # FLI, FLC
    # FPX
    # FTEX
    # GBR
    # GD
    # IM
    # IMT
    # IPTC/NAA
    # JPEG 2000
    # MCIDAS
    # MIC
    # MPO
    # MSP
    # PBM
    # PCD
    # PCX
    # PGM
    # PIXAR
    # PNM
    # PPM
    # PSD
    # SGI
    # SPIDER
    # WAL
    # WMF
    # XBM
    # XPM
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


def _check_nop(format_id, filename):
    """Format checker that always returns False (used to disable a format).

    :param str format_id: The internal format identifier to check.
    :param str filename: The path of the file to check.

    :rtype: bool
    :return: Always returns ``False``.

    > _check_nop("foo", "bar")
    False
    """
    return False


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


def get_supported_input_format_exts():
    return set(
        ext
        for fmt in IMAGES_FORMATS.values()
        if fmt["input"]
        for ext in fmt["exts"]
    )


def get_supported_output_format_ids():
    return [fid for fid, fmt in IMAGES_FORMATS.items() if fmt["output"]]


def get_supported_output_format_names():
    return [
        fmt["display_name"] for fmt in IMAGES_FORMATS.values() if fmt["output"]
    ]
