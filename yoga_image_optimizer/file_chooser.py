import os
import pathlib

from gi.repository import Gtk

from .translation import gettext as _
from .image_formats import get_supported_input_format_mimetypes
from .image_formats import get_supported_input_format_exts


def _build_file_filters():
    image_file_filter = Gtk.FileFilter()
    image_file_filter.set_name(_("Image Files"))
    if os.name == "nt":
        for ext in get_supported_input_format_exts():
            image_file_filter.add_pattern("*%s" % ext)
    else:
        for mimetype in get_supported_input_format_mimetypes():
            image_file_filter.add_mime_type(mimetype)

    any_file_filter = Gtk.FileFilter()
    any_file_filter.set_name(_("All Files"))
    any_file_filter.add_pattern("*")

    return [image_file_filter, any_file_filter]


def _build_gtk_file_chooser_open(parent=None):
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

    for filter_ in _build_file_filters():
        file_chooser_dialog.add_filter(filter_)

    return file_chooser_dialog


def _build_gtk_file_chooser_save(filename=None, parent=None):
    file_chooser_dialog = Gtk.FileChooserDialog(
        title=_("Save Image As..."),
        parent=parent,
    )
    file_chooser_dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_SAVE,
        Gtk.ResponseType.ACCEPT,
    )
    file_chooser_dialog.set_action(Gtk.FileChooserAction.SAVE)

    for filter_ in _build_file_filters():
        file_chooser_dialog.add_filter(filter_)

    if filename:
        file_chooser_dialog.set_filename(filename)
        file_chooser_dialog.set_current_name(pathlib.Path(filename).name)

    return file_chooser_dialog


def _build_win32_file_chooser_open():
    file_chooser_dialog = Gtk.FileChooserNative(
        title=_("Open Images..."),
    )
    file_chooser_dialog.set_select_multiple(True)

    for filter_ in _build_file_filters():
        file_chooser_dialog.add_filter(filter_)

    return file_chooser_dialog


def _build_win32_file_chooser_save(filename=None):
    file_chooser_dialog = Gtk.FileChooserNative(
        title=_("Save Image As..."),
    )
    file_chooser_dialog.set_action(Gtk.FileChooserAction.SAVE)

    for filter_ in _build_file_filters():
        file_chooser_dialog.add_filter(filter_)

    if filename:
        file_chooser_dialog.set_filename(filename)
        file_chooser_dialog.set_current_name(pathlib.Path(filename).name)

    return file_chooser_dialog


def open_file_chooser_open_file(parent=None):
    if os.name == "nt":
        file_chooser_dialog = _build_win32_file_chooser_open()
    else:
        file_chooser_dialog = _build_gtk_file_chooser_open(parent=parent)

    response = file_chooser_dialog.run()

    filenames = []
    if response == Gtk.ResponseType.ACCEPT:
        filenames = file_chooser_dialog.get_filenames()

    file_chooser_dialog.destroy()

    return filenames


def open_file_chooser_save_file(filename=None, parent=None):
    if os.name == "nt":
        file_chooser_dialog = _build_win32_file_chooser_save(filename=filename)
    else:
        file_chooser_dialog = _build_gtk_file_chooser_save(
            filename=filename, parent=parent
        )

    response = file_chooser_dialog.run()

    filename = None
    if response == Gtk.ResponseType.ACCEPT:
        filename = file_chooser_dialog.get_filename()

    file_chooser_dialog.destroy()

    return filename
