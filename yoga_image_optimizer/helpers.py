import os

from gi.repository import Gio


def find_data_path(path):
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, "data", path)


def human_readable_file_size(size):
    """Returns human readable file size (e.g. "11.4 kiB").

    .. NOTE::

       This function do not supports size > 1024 GiB.

    :param int size: File size in Bytes.
    :rtype: str

    >>> human_readable_file_size(123)
    '123 Bytes'
    >>> human_readable_file_size(1024)
    '1.00 kiB'
    >>> human_readable_file_size(1024 * 1024)
    '1.00 MiB'
    >>> human_readable_file_size(1024 * 1024 * 1024)
    '1.00 GiB'
    >>> human_readable_file_size(1024 + 512)
    '1.50 kiB'
    """
    if size < 1024:
        return "%i Bytes" % size
    for u, d in [("kiB", 1024 ** 1), ("MiB", 1024 ** 2), ("GiB", 1024 ** 3)]:
        if size / d < 1024:
            return "%.2f %s" % (size / d, u)
    return "∞"


def gvfs_uri_to_local_path(uri):
    """Get a local file path from a GVFS URI.

    :param str uri: A GVFS file URI.

    >>> gvfs_uri_to_local_path("file:///tmp")
    '/tmp'
    >>> gvfs_uri_to_local_path("file:///foo%20bar/baz.txt")
    '/foo bar/baz.txt'
    """
    gvfs = Gio.Vfs.get_default()
    return gvfs.get_file_for_uri(uri).get_path()
