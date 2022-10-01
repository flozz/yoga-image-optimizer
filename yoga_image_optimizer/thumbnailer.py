from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import CancelledError

from PIL import Image
from gi.repository import GLib
from gi.repository import GdkPixbuf

from . import helpers
from .data_helpers import find_data_path


THUMBNAIL_BROKEN = GdkPixbuf.Pixbuf.new_from_file(
    find_data_path("images/thumbnail_broken.svg")
)


def preview_gdk_pixbuf_from_image(image_path, size=64):
    """Returns a Gdk Pixbuf containing the preview the image at the given path.

    :param str image_path: the path of the image.
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

    image = None
    image_rgba = None

    try:
        image = helpers.open_image_from_path(image_path)
    except Exception as error:
        print(
            "E: An error occured when thumbnailing '%s': %s"
            % (image_path, str(error))
        )
    else:
        image_rgba = Image.new("RGBA", image.size)
        image_rgba.paste(image)
        image_rgba.thumbnail([size, size], Image.LANCZOS)

        # Handle JPEG orientation
        if image.format == "JPEG":
            exif = image.getexif()
            if (
                EXIF_TAG_ORIENTATION in exif
                and exif[EXIF_TAG_ORIENTATION] in ORIENTATION_OPERATIONS
            ):
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

    finally:
        if image:
            image.close()
        if image_rgba:
            image_rgba.close()

    return pixbuf


class Thumbnailer:
    _MAX_WORKERS = 1

    def __init__(self):
        # iter_: {future: future, callback: fn(iter_, pixbuf)}
        self._pending = {}
        self._executor = ThreadPoolExecutor(max_workers=self._MAX_WORKERS)

    def generate(self, iter_, image_path, callback):
        # This thumbnail has already been submitted
        if iter_ in self._pending:
            return

        def _thumbnail_callback(future):
            # The thumbnail has been canceled so we should not go further
            if iter_ not in self._pending:
                return

            try:
                pixbuf = future.result()
            except OSError as error:
                print(
                    "E: An error occured when generating thumbnail for '%s': %s"
                    % (image_path, str(error))
                )
                pixbuf = THUMBNAIL_BROKEN
            except CancelledError:
                return
            finally:
                self._pending[iter_]["callback"](iter_, pixbuf)
                del self._pending[iter_]

        future = self._executor.submit(
            preview_gdk_pixbuf_from_image, image_path
        )
        future.add_done_callback(_thumbnail_callback)

        self._pending[iter_] = {
            "future": future,
            "callback": callback,
        }

    def cancel(self, iter_):
        if iter_ not in self._pending:
            return
        self._pending[iter_]["future"].cancel()
        del self._pending[iter_]

    def cancel_all(self):
        self._pending = {}
        self._executor.shutdown(wait=False, cancel_futures=True)
        self._executor = ThreadPoolExecutor(max_workers=self._MAX_WORKERS)
