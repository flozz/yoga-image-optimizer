from pathlib import Path

from . import APPLICATION_NAME, APPLICATION_ID
from . import helpers
from . import data_helpers
from .image_formats import get_supported_output_format_ids
from .image_formats import get_supported_output_format_names

from gi.repository import Gtk, Gdk, Gio, GdkPixbuf


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
        self._builder.set_translation_domain(APPLICATION_ID)
        self._builder.add_from_file(
            data_helpers.find_data_path("ui/main-window.glade")
        )
        self._builder.connect_signals(self)

        header = self._builder.get_object("main_window_header")
        self.set_titlebar(header)

        content = self._builder.get_object("main_window_content")
        self.add(content)

        self._prepare_treeview()
        self._prepare_format_combobox()

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

        # Action: win.remove-selected-image
        action = Gio.SimpleAction.new("remove-selected-image", None)
        action.connect("activate", lambda a, p: self.remove_selected_image())
        self.add_action(action)
        self.set_accels_for_action("win.remove-selected-image", ["Delete"])

    def set_accels_for_action(self, detailed_action_name, accels):
        win_actions = self.get_action_group("win")
        action_name = detailed_action_name.split(".")[-1]

        accel_group = Gtk.AccelGroup()

        for key, mods in [Gtk.accelerator_parse(accel) for accel in accels]:
            accel_group.connect(
                key,
                mods,
                0,
                lambda *_: win_actions.activate_action(action_name),
            )

        self.add_accel_group(accel_group)

    def switch_state(self, state):
        app = self.get_application()

        # fmt: off
        if state == app.STATE_MANAGE_IMAGES:
            self._builder.get_object("add_image_button").set_sensitive(True)
            self._builder.get_object("remove_image_button").set_sensitive(True)
            self._builder.get_object("clear_images_button").set_sensitive(True)
            self._builder.get_object("optimize_button").show()
            self._builder.get_object("stop_optimization_button").hide()
            self._builder.get_object("output_image_options").set_sensitive(True)
            self._builder.get_object("jpeg_options").set_sensitive(True)
            self._builder.get_object("webp_options").set_sensitive(True)
        elif state == app.STATE_OPTIMIZE:
            self._builder.get_object("add_image_button").set_sensitive(False)
            self._builder.get_object("remove_image_button").set_sensitive(False)
            self._builder.get_object("clear_images_button").set_sensitive(False)
            self._builder.get_object("optimize_button").hide()
            self._builder.get_object("stop_optimization_button").show()
            self._builder.get_object("output_image_options").set_sensitive(False)
            self._builder.get_object("jpeg_options").set_sensitive(False)
            self._builder.get_object("webp_options").set_sensitive(False)
        # fmt: on

    def update_interface(self):
        app = self.get_application()
        output_image_options = self._builder.get_object("output_image_options")
        jpeg_options = self._builder.get_object("jpeg_options")
        webp_options = self._builder.get_object("webp_options")
        png_options = self._builder.get_object("png_options")

        # Reset output options visibilité (hide everything)
        output_image_options.hide()
        jpeg_options.hide()
        webp_options.hide()
        png_options.hide()

        # Get selected image
        iter_ = self.get_selected_image_iter()

        # No image selected, stop here
        if not iter_:
            return

        output_format = app.image_store.get(iter_)["output_format"]

        # Update and show output image options
        output_format_combobox = self._builder.get_object(
            "output_format_combobox"
        )
        output_format_combobox.set_active(
            get_supported_output_format_ids().index(output_format)
        )

        output_file = app.image_store.get(iter_)["output_file"]
        output_file_entry = self._builder.get_object("output_file_entry")
        output_file_entry.set_text(output_file)

        output_image_options.show()

        # [JPEG] Update and show jpeg options
        if output_format == "jpeg":
            jpeg_quality_adjustment = self._builder.get_object(
                "jpeg_quality_adjustment"
            )
            jpeg_quality_adjustment.set_value(
                app.image_store.get(iter_)["jpeg_quality"]
            )
            jpeg_options.show()
        # [WebP] Update and show webp options
        elif output_format == "webp":
            webp_quality_adjustment = self._builder.get_object(
                "webp_quality_adjustment"
            )
            webp_quality_adjustment.set_value(
                app.image_store.get(iter_)["webp_quality"]
            )
            webp_options.show()
        # [PNG] Update and show png options
        elif output_format == "png":
            png_slow_optimization_checkbutton = self._builder.get_object(
                "png_slow_optimization_checkbutton"
            )
            png_slow_optimization_checkbutton.set_active(
                app.image_store.get(iter_)["png_slow_optimization"]
            )
            png_options.show()

    def remove_selected_image(self):
        iter_ = self.get_selected_image_iter()
        if iter_:
            app = self.get_application()
            app.image_store.remove(iter_)

    def get_selected_image_iter(self):
        treeview_images = self._builder.get_object("images_treeview")
        selection = treeview_images.get_selection()
        if selection.count_selected_rows() == 0:
            return None
        _, iter_ = selection.get_selected()
        return iter_

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

        for output_format in get_supported_output_format_names():
            output_format_combobox.append_text(output_format)

    def _on_main_window_destroyed(self, widget):
        app = self.get_application()
        app.quit()

    def _on_drag_data_received(
        self, widget, drag_context, x, y, data, info, time
    ):
        app = self.get_application()

        def _add_path(paths):
            for path in paths:
                if path.is_dir():
                    _add_path(p for p in path.glob("**/*") if p.is_file())
                elif path.is_file():
                    app.add_image(path)
                    Gtk.main_iteration_do(True)

        for uri in data.get_uris():
            path = Path(helpers.gvfs_uri_to_local_path(uri))
            _add_path([path])

    def _on_image_treeview_selection_changed(self, selection):
        self.update_interface()

    def _on_output_file_entry_changed(self, entry):
        app = self.get_application()
        iter_ = self.get_selected_image_iter()
        output_file = Path(entry.get_text())
        app.image_store.update(
            iter_,
            output_file=output_file.resolve().as_posix(),
        )

    def _on_output_format_combobox_changed(self, combobox):
        app = self.get_application()
        iter_ = self.get_selected_image_iter()
        output_format_combobox = self._builder.get_object(
            "output_format_combobox"
        )

        output_format = get_supported_output_format_ids()[
            output_format_combobox.get_active()
        ]

        app.image_store.update(iter_, output_format=output_format)
        self.update_interface()

    def _on_jpeg_quality_adjustement_value_changed(self, adjustement):
        app = self.get_application()
        iter_ = self.get_selected_image_iter()
        app.image_store.update(iter_, jpeg_quality=adjustement.get_value())

    def _on_webp_quality_adjustement_value_changed(self, adjustement):
        app = self.get_application()
        iter_ = self.get_selected_image_iter()
        app.image_store.update(iter_, webp_quality=adjustement.get_value())

    def _on_png_slow_optimization_checkbutton_toggled(self, checkbutton):
        app = self.get_application()
        iter_ = self.get_selected_image_iter()
        app.image_store.update(
            iter_, png_slow_optimization=checkbutton.get_active()
        )
