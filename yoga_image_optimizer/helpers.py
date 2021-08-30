from PIL import Image
from gi.repository import GLib
from gi.repository import Gio
from gi.repository import GdkPixbuf

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
        (_("kiB"), 1024 ** 1),
        (_("MiB"), 1024 ** 2),
        (_("GiB"), 1024 ** 3),
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


def open_image_from_path(path):
    """Open a PIL image from the given path.

    TODO: Handle JPEG rotation

    :param str path: The path of the image.

    :rtype: PIL.Image.Image
    """
    return Image.open(path)


def preview_gdk_pixbuf_from_image(image, size=64):
    """Returns a Gdk Pixbuf containing the preview the image at the given path.

    :param PIL.Image.Image image: the image.
    :param int size: The size of the preview (optional, default: ``64``).

    :rtype: GdkPixbuf.Pixbuff
    """
    EXIF_TAG_ORIENTATION = 274
    ORIENTATION_OPERATIONS = {
        1: [],
        2: [Image.FLIP_LEFT_RIGHT],
        3: [Image.ROTATE_180],
        4: [Image.FLIP_TOP_BOTTOM],
        5: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
        6: [Image.ROTATE_270],
        7: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_270],
        8: [Image.ROTATE_90],
    }

    image_rgba = Image.new("RGBA", image.size)
    image_rgba.paste(image)
    image_rgba.thumbnail([size, size], Image.LANCZOS)

    # Handle JPEG orientation
    if image.format == "JPEG":
        exif = image.getexif()
        if EXIF_TAG_ORIENTATION in exif:
            orientation = exif[EXIF_TAG_ORIENTATION]
            for operation in ORIENTATION_OPERATIONS[orientation]:
                image_rgba = image_rgba.transpose(operation)

    # fmt: off
    pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(
        GLib.Bytes.new(image_rgba.tobytes()),  # data
        GdkPixbuf.Colorspace.RGB,              # colorspace
        True,                                  # has alpha
        8,                                     # bits_per_sample
        *image_rgba.size,                      # width, height
        image_rgba.size[0] * 4,                # rowstride
    )
    # fmt: on

    image_rgba.close()

    return pixbuf
