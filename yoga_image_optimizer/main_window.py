import os

from . import APPLICATION_NAME
from . import helpers

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa: E402


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self,
            application=app,
            title=APPLICATION_NAME,
            # icon_name="TODO",
            default_width=800,
            default_height=500,
            resizable=True)

        self._builder = Gtk.Builder()
        self._builder.add_from_file(helpers.find_data_path("ui/main-window.glade"))  # noqa: E501
        self._builder.connect_signals(self)

        header = self._builder.get_object("main-window-header")
        self.set_titlebar(header)

        content = self._builder.get_object("main-window-content")
        self.add(content)

        self._prepare_treeview()

        open_image_dialog = self._builder.get_object("open_image_dialog")
        open_image_dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.connect("destroy", self._on_main_window_destroyed)

        # Drag & drop files
        self.drag_dest_set(
                Gtk.DestDefaults.ALL,
                [Gtk.TargetEntry.new(
                    "text/uri-list",
                    Gtk.TargetFlags.OTHER_APP,
                    0)],
                Gdk.DragAction.COPY)
        self.connect("drag-data-received", self._on_drag_data_received)

    def switch_state(self, state):
        app = self.get_application()

        if state == app.STATE_MANAGE_IMAGES:
            self._builder.get_object("add_image_button").set_sensitive(True)
            self._builder.get_object("remove_image_button").set_sensitive(True)
            self._builder.get_object("clear_images_button").set_sensitive(True)
            self._builder.get_object("optimize_button").show()
            self._builder.get_object("stop_optimization_button").hide()
            self._builder.get_object("images_treeview").set_sensitive(True)
        elif state == app.STATE_OPTIMIZE:
            self._builder.get_object("add_image_button").set_sensitive(False)
            self._builder.get_object("remove_image_button").set_sensitive(False)  # noqa: E501
            self._builder.get_object("clear_images_button").set_sensitive(False)  # noqa: E501
            self._builder.get_object("optimize_button").hide()
            self._builder.get_object("stop_optimization_button").show()
            self._builder.get_object("images_treeview").set_sensitive(False)
            self._builder.get_object("open_image_dialog").hide()

    def _prepare_treeview(self):
        app = self.get_application()

        treeview_images = self._builder.get_object("images_treeview")
        treeview_images.set_model(app.image_store.gtk_list_store)

        # Status
        treeview_images.append_column(Gtk.TreeViewColumn(
                app.image_store.FIELDS["status_display"]["label"],
                Gtk.CellRendererText(),
                text=app.image_store.FIELDS["status_display"]["id"]))

        # Preview
        renderer_prevew = Gtk.CellRendererPixbuf()
        column_preview = Gtk.TreeViewColumn(None, renderer_prevew)
        column_preview.add_attribute(
                renderer_prevew,
                "pixbuf",
                app.image_store.FIELDS["preview"]["id"])
        treeview_images.append_column(column_preview)

        # Input Image
        treeview_images.append_column(Gtk.TreeViewColumn(
                app.image_store.FIELDS["input_file_display"]["label"],
                Gtk.CellRendererText(),
                text=app.image_store.FIELDS["input_file_display"]["id"]))

        # Input Size
        treeview_images.append_column(Gtk.TreeViewColumn(
                app.image_store.FIELDS["input_size_display"]["label"],
                Gtk.CellRendererText(),
                text=app.image_store.FIELDS["input_size_display"]["id"]))

        # ->
        treeview_images.append_column(Gtk.TreeViewColumn(

                app.image_store.FIELDS["separator"]["label"],
                Gtk.CellRendererText(),
                text=app.image_store.FIELDS["separator"]["id"]))

        # Output Image
        treeview_images.append_column(Gtk.TreeViewColumn(
                app.image_store.FIELDS["output_file_display"]["label"],
                Gtk.CellRendererText(),
                text=app.image_store.FIELDS["output_file_display"]["id"]))

        # Output Format
        treeview_images.append_column(Gtk.TreeViewColumn(
                app.image_store.FIELDS["output_format_display"]["label"],
                Gtk.CellRendererText(),
                text=app.image_store.FIELDS["output_format_display"]["id"]))

        # Output Size
        treeview_images.append_column(Gtk.TreeViewColumn(
                app.image_store.FIELDS["output_size_display"]["label"],
                Gtk.CellRendererText(),
                text=app.image_store.FIELDS["output_size_display"]["id"]))

    def _on_add_image_button_clicked(self, widget):
        open_image_dialog = self._builder.get_object("open_image_dialog")
        open_image_dialog.show_all()

    def _on_remove_image_button_clicked(self, widget):
        treeview_images = self._builder.get_object("images_treeview")
        selection = treeview_images.get_selection()

        if selection.count_selected_rows() == 0:
            return

        store, iter_ = selection.get_selected()
        store.remove(iter_)

    def _on_clear_images_button_clicked(self, widget):
        app = self.get_application()
        app.image_store.clear()

    def _on_optimize_button_clicked(self, widget):
        app = self.get_application()
        app.optimize()

    def _on_stop_optimization_button_clicked(self, widget):
        app = self.get_application()
        app.stop_optimization()

    def _on_open_image_dialog_response(self, widget, response):
        widget.hide()
        app = self.get_application()
        print("RESPONSE", response)
        if response == Gtk.ResponseType.OK:
            for file_ in widget.get_filenames():
                app.add_image(file_)

    def _on_main_window_destroyed(self, widget):
        app = self.get_application()
        app.stop_optimization()

    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):  # noqa: E501
        app = self.get_application()
        for uri in data.get_uris():
            path = helpers.gvfs_uri_to_local_path(uri)
            if not os.path.isfile(path):
                continue
            app.add_image(path)

    def _on_image_treeview_selection_changed(self, selection):
        _COMBOBOX_FORMATS = {
            "JPEG": 0,
            "PNG": 1,
        }

        app = self.get_application()
        _, iter_ = selection.get_selected()
        output_image_options = self._builder.get_object("output_image_options")
        output_format_combobox = self._builder.get_object("output_format_combobox")
        output_file_entry = self._builder.get_object("output_file_entry")

        if not iter_:
            output_image_options.hide()
            return
        else:
            output_image_options.show()

        output_format_combobox.set_active(_COMBOBOX_FORMATS[app.image_store.get(iter_)["output_format"]])

        output_file = app.image_store.get(iter_)["output_file"]
        output_file_entry.set_text(output_file)

    def _on_output_file_entry_changed(self, entry):
        app = self.get_application()
        treeview_images = self._builder.get_object("images_treeview")
        selection = treeview_images.get_selection()
        _, iter_ = selection.get_selected()

        output_file = os.path.abspath(entry.get_text())

        app.image_store.update(
            iter_,
            output_file=output_file,
        )

    def _on_output_format_combobox_changed(self, combobox):
        _COMBOBOX_FORMATS = {
            0: "JPEG",
            1: "PNG",
        }

        app = self.get_application()
        treeview_images = self._builder.get_object("images_treeview")
        selection = treeview_images.get_selection()
        _, iter_ = selection.get_selected()

        output_format_combobox = self._builder.get_object("output_format_combobox")

        output_format_index = output_format_combobox.get_active()
        output_format = _COMBOBOX_FORMATS[output_format_index]

        app.image_store.update(
            iter_,
            output_format=output_format,
        )

        self._on_image_treeview_selection_changed(selection)
