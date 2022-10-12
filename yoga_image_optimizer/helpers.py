import os
import hashlib

from PIL import Image
from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

from .translation import gettext as _
from .translation import format_string


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
        return "%i %s" % (size, _("Bytes"))
    for u, d in [
        (_("kiB"), 1024**1),
        (_("MiB"), 1024**2),
        (_("GiB"), 1024**3),
    ]:
        if size / d < 1024:
            return "%s %s" % (format_string("%.2f", size / d), u)
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


def local_path_to_gvfs_uri(path):
    """Get a GVFS URI from a local file path.

    :param str path: The local file path.

    >>> local_path_to_gvfs_uri("/tmp")
    'file:///tmp'
    >>> local_path_to_gvfs_uri("/foo bar/baz.txt")
    'file:///foo%20bar/baz.txt'
    """
    gvfs = Gio.Vfs.get_default()
    return gvfs.get_file_for_path(path).get_uri()


def get_thumbnail_path_for_file(path, size="normal"):
    """Get the path of the cached thumbnail for the given file and size.

    :param str path: The file path.
    :param str size: The thumbnail size ("normal", "large", "x-large"
                     or "xx-large")

    >>> get_thumbnail_path_for_file("/foo.png")
    '/home/.../.cache/thumbnails/normal/9a813ff0dc14ccc96494338dde9f6324.png'
    >>> get_thumbnail_path_for_file("/foo.png", size="large")
    '/home/.../.cache/thumbnails/large/9a813ff0dc14ccc96494338dde9f6324.png'
    >>> get_thumbnail_path_for_file("/foo.png", size="x-large")
    '/home/.../.cache/thumbnails/x-large/9a813ff0dc14ccc96494338dde9f6324.png'
    >>> get_thumbnail_path_for_file("/foo.png", size="xx-large")
    '/home/.../.cache/thumbnails/xx-large/9a813ff0dc14ccc96494338dde9f6324.png'
    >>> get_thumbnail_path_for_file("/foo.png", size="foobar")
    Traceback (most recent call last):
        ...
    ValueError: Invalid size 'foobar'
    """
    if size not in ["normal", "large", "x-large", "xx-large"]:
        raise ValueError("Invalid size '%s'" % str(size))
    cache_dir = GLib.get_user_cache_dir()
    file_uri = local_path_to_gvfs_uri(path)
    file_uri_md5 = hashlib.md5(file_uri.encode("UTF-8")).hexdigest()
    return os.path.join(cache_dir, "thumbnails", size, "%s.png" % file_uri_md5)


def open_image_from_path(path):
    """Open a PIL image from the given path.

    TODO: Handle JPEG rotation

    :param str path: The path of the image.

    :rtype: PIL.Image.Image
    """
    return Image.open(path)


def load_gtk_custom_css(path):
    """Load custom GTK CSS from path.

    :param str path: Path to the CSS file.
    """
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(path)
    screen = Gdk.Screen.get_default()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(
        screen,
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER,
    )
