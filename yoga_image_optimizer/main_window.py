from pathlib import Path

from . import APPLICATION_NAME
from . import helpers

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf  # noqa: E402


OUTPUT_FORMATS = [
    "JPEG",
    "PNG",
]


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self,
            application=app,
            title=APPLICATION_NAME,
            # icon_name="TODO",
            default_width=800,
            default_height=500,
            resizable=True,
        )

        self._builder = Gtk.Builder()
        self._builder.add_from_file(
            helpers.find_data_path("ui/main-window.glade")
        )
        self._builder.connect_signals(self)

        header = self._builder.get_object("main-window-header")
        self.set_titlebar(header)

        content = self._builder.get_object("main-window-content")
        self.add(content)

        self._prepare_treeview()
        self._prepare_format_combobox()

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
            [
                Gtk.TargetEntry.new(
                    "text/uri-list",
                    Gtk.TargetFlags.OTHER_APP,
                    0,
                )
            ],
            Gdk.DragAction.COPY,
        )
        self.connect("drag-data-received", self._on_drag_data_received)

    def switch_state(self, state):
        app = self.get_application()

        # fmt: off
        if state == app.STATE_MANAGE_IMAGES:
            self._builder.get_object("add_image_button").set_sensitive(True)
            self._builder.get_object("remove_image_button").set_sensitive(True)
            self._builder.get_object("clear_images_button").set_sensitive(True)
            self._builder.get_object("optimize_button").show()
            self._builder.get_object("stop_optimization_button").hide()
            self._builder.get_object("images_treeview").set_sensitive(True)
        elif state == app.STATE_OPTIMIZE:
            self._builder.get_object("add_image_button").set_sensitive(False)
            self._builder.get_object("remove_image_button").set_sensitive(False)
            self._builder.get_object("clear_images_button").set_sensitive(False)
            self._builder.get_object("optimize_button").hide()
            self._builder.get_object("stop_optimization_button").show()
            self._builder.get_object("images_treeview").set_sensitive(False)
            self._builder.get_object("open_image_dialog").hide()
        # fmt: on

    def _prepare_treeview(self):
        app = self.get_application()

        DISPLAYED_FIELDS = [
            "status_display",
            "preview",
            "input_file_display",
            "input_size_display",
            "separator",
            "output_file_display",
            "output_format_display",
            "output_size_display",
        ]

        treeview_images = self._builder.get_object("images_treeview")
        treeview_images.set_model(app.image_store.gtk_list_store)

        for field_name in DISPLAYED_FIELDS:
            field_type = app.image_store.FIELDS[field_name]["type"]

            if field_type is str:
                treeview_images.append_column(
                    Gtk.TreeViewColumn(
                        app.image_store.FIELDS[field_name]["label"],
                        Gtk.CellRendererText(),
                        text=app.image_store.FIELDS[field_name]["id"],
                    ),
                )
            elif field_type is GdkPixbuf.Pixbuf:
                pixbuf = Gtk.CellRendererPixbuf()
                column = Gtk.TreeViewColumn(
                    app.image_store.FIELDS[field_name]["label"],
                    pixbuf,
                )
                column.add_attribute(
                    pixbuf,
                    "pixbuf",
                    app.image_store.FIELDS[field_name]["id"],
                )
                treeview_images.append_column(column)
            else:
                raise TypeError(
                    "Unsupported field type '%s'" % str(field_type)
                )

    def _prepare_format_combobox(self):
        output_format_combobox = self._builder.get_object(
            "output_format_combobox"
        )

        for output_format in OUTPUT_FORMATS:
            output_format_combobox.append_text(output_format)

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

    def _on_drag_data_received(
        self, widget, drag_context, x, y, data, info, time
    ):
        app = self.get_application()
        for uri in data.get_uris():
            path = Path(helpers.gvfs_uri_to_local_path(uri))
            if not path.is_file():
                continue
            app.add_image(path)

    def _on_image_treeview_selection_changed(self, selection):
        app = self.get_application()
        _, iter_ = selection.get_selected()
        output_image_options = self._builder.get_object("output_image_options")
        output_format_combobox = self._builder.get_object(
            "output_format_combobox"
        )
        output_file_entry = self._builder.get_object("output_file_entry")

        if not iter_:
            output_image_options.hide()
            return
        else:
            output_image_options.show()

        output_format_combobox.set_active(
            OUTPUT_FORMATS.index(app.image_store.get(iter_)["output_format"])
        )

        output_file = app.image_store.get(iter_)["output_file"]
        output_file_entry.set_text(output_file)

    def _on_output_file_entry_changed(self, entry):
        app = self.get_application()
        treeview_images = self._builder.get_object("images_treeview")
        selection = treeview_images.get_selection()
        _, iter_ = selection.get_selected()

        output_file = Path(entry.get_text())

        app.image_store.update(
            iter_,
            output_file=output_file.resolve().as_posix(),
        )

    def _on_output_format_combobox_changed(self, combobox):
        app = self.get_application()
        treeview_images = self._builder.get_object("images_treeview")
        selection = treeview_images.get_selection()
        _, iter_ = selection.get_selected()

        output_format_combobox = self._builder.get_object(
            "output_format_combobox"
        )

        output_format = OUTPUT_FORMATS[output_format_combobox.get_active()]

        app.image_store.update(
            iter_,
            output_format=output_format,
        )

        self._on_image_treeview_selection_changed(selection)
