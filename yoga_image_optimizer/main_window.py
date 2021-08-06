import os
from pathlib import Path

from gi.repository import Gtk, Gdk, Gio, GdkPixbuf

from . import APPLICATION_NAME, APPLICATION_ID
from . import helpers
from . import data_helpers
from . import config
from .image_formats import get_supported_output_format_ids
from .image_formats import get_supported_output_format_names
from .translation import gtk_builder_translation_hack
from .translation import gettext as _
from .custom_pattern_dialog import CustomPatternDialog
from .file_chooser import open_file_chooser_save_file


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self,
            application=app,
            title=APPLICATION_NAME,
            icon=GdkPixbuf.Pixbuf.new_from_file(
                data_helpers.find_data_path("images/icon_64.png")
            ),
            default_width=1000,
            default_height=600,
            resizable=True,
        )

        self._updating_interface = False

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
        action = Gio.SimpleAction.new("remove-selected-images", None)
        action.connect(
            "activate", self._on_remove_selected_images_action_activated
        )
        self.add_action(action)

        images_treeview = self._builder.get_object("images_treeview")
        self.set_accels_for_action_while_widget_focused(
            "win.remove-selected-images",
            ["Delete"],
            images_treeview,
        )

        # HACK: Translate the UI on Windows
        if os.name == "nt":
            gtk_builder_translation_hack(self._builder)

    def set_accels_for_action_while_widget_focused(
        self, detailed_action_name, accels, widget
    ):
        action_group_name, action_name = detailed_action_name.split(".")
        action_group = self.get_action_group(action_group_name)

        accel_group = Gtk.AccelGroup()

        for key, mods in [Gtk.accelerator_parse(accel) for accel in accels]:
            accel_group.connect(
                key,
                mods,
                0,
                # Activate the action only if the widget is focused
                lambda *_: widget.has_focus()
                and action_group.activate_action(action_name),
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
            self._builder.get_object("png_options").set_sensitive(True)
        elif state == app.STATE_OPTIMIZE:
            self._builder.get_object("add_image_button").set_sensitive(False)
            self._builder.get_object("remove_image_button").set_sensitive(False)
            self._builder.get_object("clear_images_button").set_sensitive(False)
            self._builder.get_object("optimize_button").hide()
            self._builder.get_object("stop_optimization_button").show()
            self._builder.get_object("output_image_options").set_sensitive(False)
            self._builder.get_object("jpeg_options").set_sensitive(False)
            self._builder.get_object("webp_options").set_sensitive(False)
            self._builder.get_object("png_options").set_sensitive(False)
        # fmt: on

    def update_interface(self):
        self._updating_interface = True

        app = self.get_application()
        output_image_options = self._builder.get_object("output_image_options")
        jpeg_options = self._builder.get_object("jpeg_options")
        webp_options = self._builder.get_object("webp_options")
        png_options = self._builder.get_object("png_options")

        def _have_all_same_values(iters, property_):
            value = app.image_store.get(iters[0])[property_]
            for iter_ in iters:
                if app.image_store.get(iter_)[property_] != value:
                    return False
            return True

        def _avg(iters, property_):
            return sum(
                [app.image_store.get(iter_)[property_] for iter_ in iters]
            ) // len(iters)

        # Reset output options visibility (hide everything)
        output_image_options.hide()
        jpeg_options.hide()
        webp_options.hide()
        png_options.hide()

        # Get selected images
        iters = self.get_selected_image_iters()

        # No image selected, stop here
        if len(iters) == 0:
            return

        if _have_all_same_values(iters, "output_format"):
            output_format = app.image_store.get(iters[0])["output_format"]
        else:
            output_format = None

        # [Output image] Update and show output image options
        output_format_combobox = self._builder.get_object(
            "output_format_combobox"
        )
        if output_format is not None:
            output_format_combobox.set_active(
                get_supported_output_format_ids().index(output_format)
            )
        else:
            output_format_combobox.set_active(-1)

        resize_checkbutton = self._builder.get_object("resize_checkbutton")
        if _have_all_same_values(iters, "resize_enabled"):
            resize_checkbutton.set_active(
                app.image_store.get(iters[0])["resize_enabled"]
            )
            resize_checkbutton.set_inconsistent(False)
        else:
            resize_checkbutton.set_active(False)
            resize_checkbutton.set_inconsistent(True)

        resize_width_adjustment = self._builder.get_object(
            "resize_width_adjustment"
        )
        resize_width_adjustment.set_value(
            max(
                [app.image_store.get(iter_)["resize_width"] for iter_ in iters]
            )
        )

        resize_width_spinbutton = self._builder.get_object(
            "resize_width_spinbutton"
        )
        resize_width_spinbutton.set_sensitive(resize_checkbutton.get_active())

        resize_height_adjustment = self._builder.get_object(
            "resize_height_adjustment"
        )
        resize_height_adjustment.set_value(
            max(
                [
                    app.image_store.get(iter_)["resize_height"]
                    for iter_ in iters
                ]
            )
        )

        resize_height_spinbutton = self._builder.get_object(
            "resize_height_spinbutton"
        )
        resize_height_spinbutton.set_sensitive(resize_checkbutton.get_active())

        resize_reset_button = self._builder.get_object("resize_reset_button")
        if len(iters) > 1:
            resize_reset_button.set_visible(True)
        elif (
            app.image_store.get(iters[0])["resize_width"]
            != app.image_store.get(iters[0])["image_width"]
            or app.image_store.get(iters[0])["resize_height"]
            != app.image_store.get(iters[0])["image_height"]
        ):
            resize_reset_button.set_visible(True)
        else:
            resize_reset_button.set_visible(False)

        output_file_entry = self._builder.get_object("output_file_entry")
        if len(iters) == 1:
            output_file = app.image_store.get(iters[0])["output_file"]
            output_file_entry.set_text(output_file)
            output_file_entry.set_sensitive(True)
        else:
            output_file_entry.set_text(_("— Multiple files selected —"))
            output_file_entry.set_sensitive(False)

        output_image_options.show()

        output_path_browse_modelbutton = self._builder.get_object(
            "output_path_browse_modelbutton"
        )
        output_path_browse_modelbutton.set_sensitive(len(iters) == 1)

        # [JPEG] Update and show jpeg options
        if output_format == "jpeg":
            jpeg_quality_adjustment = self._builder.get_object(
                "jpeg_quality_adjustment"
            )
            jpeg_quality_adjustment.set_value(_avg(iters, "jpeg_quality"))
            jpeg_options.show()
        # [WebP] Update and show webp options
        elif output_format == "webp":
            webp_quality_adjustment = self._builder.get_object(
                "webp_quality_adjustment"
            )
            webp_quality_adjustment.set_value(_avg(iters, "webp_quality"))
            webp_options.show()
        # [PNG] Update and show png options
        elif output_format == "png":
            png_slow_optimization_checkbutton = self._builder.get_object(
                "png_slow_optimization_checkbutton"
            )
            if _have_all_same_values(iters, "png_slow_optimization"):
                png_slow_optimization_checkbutton.set_active(
                    app.image_store.get(iters[0])["png_slow_optimization"]
                )
                png_slow_optimization_checkbutton.set_inconsistent(False)
            else:
                png_slow_optimization_checkbutton.set_active(False)
                png_slow_optimization_checkbutton.set_inconsistent(True)
            png_options.show()

        self._updating_interface = False

    def remove_selected_images(self):
        app = self.get_application()
        if not app.current_state == app.STATE_MANAGE_IMAGES:
            return

        iters = self.get_selected_image_iters()
        for iter_ in iters:
            app = self.get_application()
            app.image_store.remove(iter_)

    def get_selected_image_iters(self):
        treeview_images = self._builder.get_object("images_treeview")
        selection = treeview_images.get_selection()
        model = treeview_images.get_model()

        _, tree_paths = selection.get_selected_rows()
        return [model.get_iter(tree_path) for tree_path in tree_paths]

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

        # Enable multi-selection
        selection = treeview_images.get_selection()
        selection.set_mode(Gtk.SelectionMode.MULTIPLE)

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

    def _on_output_format_combobox_changed(self, combobox):
        if self._updating_interface:
            return

        app = self.get_application()
        output_format_combobox = self._builder.get_object(
            "output_format_combobox"
        )

        # No format selected
        if output_format_combobox.get_active() == -1:
            return

        output_format = get_supported_output_format_ids()[
            output_format_combobox.get_active()
        ]

        iters = self.get_selected_image_iters()
        for iter_ in iters:
            app.image_store.update(iter_, output_format=output_format)
            app.image_store.reset_status(iter_)

        self.update_interface()

    def _on_resize_checkbutton_toggled(self, checkbutton):
        if self._updating_interface:
            return

        app = self.get_application()
        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_, resize_enabled=checkbutton.get_active()
            )
            app.image_store.reset_status(iter_)

        self.update_interface()

    def _on_resize_width_adjustment_value_changed(self, adjustment):
        if self._updating_interface:
            return

        app = self.get_application()
        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_, resize_width=round(adjustment.get_value())
            )
            app.image_store.reset_status(iter_)

        self.update_interface()

    def _on_resize_height_adjustment_value_changed(self, adjustment):
        if self._updating_interface:
            return

        app = self.get_application()
        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_, resize_height=round(adjustment.get_value())
            )
            app.image_store.reset_status(iter_)

        self.update_interface()

    def _on_resize_reset_button_clicked(self, widget):
        if self._updating_interface:
            return

        app = self.get_application()
        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_,
                resize_width=app.image_store.get(iter_)["image_width"],
                resize_height=app.image_store.get(iter_)["image_height"],
            )
            app.image_store.reset_status(iter_)

        self.update_interface()

    def _on_output_file_entry_changed(self, entry):
        if self._updating_interface:
            return

        app = self.get_application()
        iters = self.get_selected_image_iters()

        if len(iters) != 1:
            return

        output_file = Path(entry.get_text())
        app.image_store.update(
            iters[0],
            output_file=str(output_file.resolve()),
            use_output_pattern=False,
        )
        app.image_store.reset_status(iters[0])

    def _on_output_pattern_next_to_file_modelbutton_clicked(self, widget):
        app = self.get_application()
        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_,
                output_pattern=config.DEFAULT_OUTPUT_PATTERNS["next-to-file"],
                use_output_pattern=True,
            )
            app.image_store.reset_status(iter_)

        if len(iters) == 1:
            output_file_entry = self._builder.get_object("output_file_entry")
            output_file_entry.set_text(
                app.image_store.get(iters[0])["output_file"]
            )

    def _on_output_pattern_subfolder_modelbutton_clicked(self, widget):
        app = self.get_application()
        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_,
                output_pattern=config.DEFAULT_OUTPUT_PATTERNS["subfolder"],
                use_output_pattern=True,
            )
            app.image_store.reset_status(iter_)

        if len(iters) == 1:
            output_file_entry = self._builder.get_object("output_file_entry")
            output_file_entry.set_text(
                app.image_store.get(iters[0])["output_file"]
            )

    def _on_output_pattern_custom_modelbutton_clicked(self, widget):
        app = self.get_application()

        custom_pattern_dialog = CustomPatternDialog(
            initial_pattern=app.config.get("output", "custom-pattern"),
            parent_window=self,
        )
        custom_pattern = custom_pattern_dialog.run()

        if not custom_pattern:
            return

        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_,
                output_pattern=custom_pattern,
                use_output_pattern=True,
            )
            app.image_store.reset_status(iter_)

        if len(iters) == 1:
            output_file_entry = self._builder.get_object("output_file_entry")
            output_file_entry.set_text(
                app.image_store.get(iters[0])["output_file"]
            )

    def _on_output_path_browse_modelbutton_clicked(self, widget):
        app = self.get_application()
        iter_ = self.get_selected_image_iters()[0]

        filename = open_file_chooser_save_file(
            filename=app.image_store.get(iter_)["output_file"],
            parent=self,
        )

        if filename:
            app.image_store.update(
                iter_,
                output_file=filename,
                use_output_pattern=False,
            )
            output_file_entry = self._builder.get_object("output_file_entry")
            output_file_entry.set_text(
                app.image_store.get(iter_)["output_file"]
            )

    def _on_jpeg_quality_adjustement_value_changed(self, adjustment):
        if self._updating_interface:
            return

        app = self.get_application()
        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_, jpeg_quality=round(adjustment.get_value())
            )
            app.image_store.reset_status(iter_)

    def _on_webp_quality_adjustement_value_changed(self, adjustment):
        if self._updating_interface:
            return

        app = self.get_application()
        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_, webp_quality=round(adjustment.get_value())
            )
            app.image_store.reset_status(iter_)

    def _on_png_slow_optimization_checkbutton_toggled(self, checkbutton):
        if self._updating_interface:
            return

        app = self.get_application()
        iters = self.get_selected_image_iters()

        for iter_ in iters:
            app.image_store.update(
                iter_, png_slow_optimization=checkbutton.get_active()
            )
            app.image_store.reset_status(iter_)

        self.update_interface()

    def _on_remove_selected_images_action_activated(self, action, param):
        self.remove_selected_images()
