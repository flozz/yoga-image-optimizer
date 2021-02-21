from . import APPLICATION_NAME
from .helpers import find_data_path

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf  # noqa: E402


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self,
            application=app,
            title=APPLICATION_NAME,
            # icon_name="TODO",
            default_width=600,
            default_height=500,
            resizable=True)

        self._builder = Gtk.Builder()
        self._builder.add_from_file(find_data_path("ui/main-window.glade"))
        self._builder.connect_signals(self)

        header = self._builder.get_object("main-window-header")
        self.set_titlebar(header)

        content = self._builder.get_object("main-window-content")
        self.add(content)

        self._prepare_treeview()

    def _prepare_treeview(self):
        self._image_store = Gtk.ListStore(
                GdkPixbuf.Pixbuf,  # Preview
                str,               # Input Image
                str,               # Input Format
                str,               # ->
                str,               # Output File
                str,               # Output Format
                str,               # Status
                )

        treeview_images = self._builder.get_object("treeview-images")
        treeview_images.set_model(self._image_store)

        # Preview
        renderer_prevew = Gtk.CellRendererPixbuf()
        column_preview = Gtk.TreeViewColumn(None, renderer_prevew)
        column_preview.add_attribute(renderer_prevew, "pixbuf", 0)
        treeview_images.append_column(column_preview)

        # Input Image
        renderer_input_image = Gtk.CellRendererText()
        column_input_image = Gtk.TreeViewColumn(
                "Input Image",
                renderer_input_image,
                text=1)
        treeview_images.append_column(column_input_image)

        # Input Format
        renderer_input_format = Gtk.CellRendererText()
        column_input_format = Gtk.TreeViewColumn(
                "Input Format",
                renderer_input_format,
                text=2)
        treeview_images.append_column(column_input_format)

        # ->
        renderer_separator = Gtk.CellRendererText()
        column_separator = Gtk.TreeViewColumn(
                None,
                renderer_separator,
                text=3)
        treeview_images.append_column(column_separator)

        # Output Image
        renderer_output_image = Gtk.CellRendererText()
        column_output_image = Gtk.TreeViewColumn(
                "Output Image",
                renderer_output_image,
                text=4)
        treeview_images.append_column(column_output_image)

        # Output Format
        renderer_output_format = Gtk.CellRendererText()
        column_output_format = Gtk.TreeViewColumn(
                "Output Format",
                renderer_output_format,
                text=5)
        treeview_images.append_column(column_output_format)

        # Status
        renderer_status = Gtk.CellRendererText()
        column_status = Gtk.TreeViewColumn("Status", renderer_status, text=6)
        treeview_images.append_column(column_status)
