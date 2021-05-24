import os

from gi.repository import Gtk

from .translation import gettext as _
from .image_formats import get_supported_input_format_mimetypes
from .image_formats import get_supported_input_format_exts


def _build_gtk_file_chooser(parent=None):
    file_chooser_dialog = Gtk.FileChooserDialog(
        title=_("Open Images..."),
        parent=parent,
    )
    file_chooser_dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,
        Gtk.ResponseType.ACCEPT,
    )
    file_chooser_dialog.set_select_multiple(True)

    image_file_filter = Gtk.FileFilter()
    image_file_filter.set_name(_("Image Files"))
    for mimetype in get_supported_input_format_mimetypes():
        image_file_filter.add_mime_type(mimetype)
    file_chooser_dialog.add_filter(image_file_filter)

    any_file_filter = Gtk.FileFilter()
    any_file_filter.set_name(_("All Files"))
    any_file_filter.add_pattern("*")
    file_chooser_dialog.add_filter(any_file_filter)

    return file_chooser_dialog


def _build_win32_file_chooser():
    file_chooser_dialog = Gtk.FileChooserNative(
        title=_("Open Images..."),
    )

    file_chooser_dialog.set_select_multiple(True)

    image_file_filter = Gtk.FileFilter()
    image_file_filter.set_name(_("Image Files"))
    for ext in get_supported_input_format_exts():
        image_file_filter.add_pattern("*%s" % ext)
    file_chooser_dialog.add_filter(image_file_filter)

    any_file_filter = Gtk.FileFilter()
    any_file_filter.set_name(_("All Files"))
    any_file_filter.add_pattern("*")
    file_chooser_dialog.add_filter(any_file_filter)

    return file_chooser_dialog


def open_file_chooser(parent=None):
    if os.name == "nt":
        file_chooser_dialog = _build_win32_file_chooser()
    else:
        file_chooser_dialog = _build_gtk_file_chooser(parent=parent)

    response = file_chooser_dialog.run()

    filenames = []
    if response == Gtk.ResponseType.ACCEPT:
        filenames = file_chooser_dialog.get_filenames()

    file_chooser_dialog.destroy()

    return filenames
