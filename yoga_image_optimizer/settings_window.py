import os

from gi.repository import Gtk, GdkPixbuf

from . import APPLICATION_NAME, APPLICATION_ID
from . import data_helpers
from . import gtk_themes_helpers
from .translation import gtk_builder_translation_hack
from .translation import gettext as _
from .config import save_config


class SettingsWindow(Gtk.Window):
    def __init__(self, config, parent_window=None):
        Gtk.Window.__init__(
            self,
            title="%s - %s" % (_("Settings"), APPLICATION_NAME),
            icon=GdkPixbuf.Pixbuf.new_from_file(
                data_helpers.find_data_path("images/icon_64.png")
            ),
            default_width=450,
            modal=True,
        )
        self.set_transient_for(parent_window)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

        self._config = config

        self._builder = Gtk.Builder()
        self._builder.set_translation_domain(APPLICATION_ID)
        self._builder.add_from_file(
            data_helpers.find_data_path("ui/settings-window.glade")
        )
        self._builder.connect_signals(self)

        content = self._builder.get_object("settings_window_content")
        self.add(content)

        self._prepare_theme_combobox()
        self.update_interface()

        self.connect("destroy", self._on_settings_windows_destroyed)

        # HACK: Translate the UI on Windows
        if os.name == "nt":
            gtk_builder_translation_hack(self._builder)

    def destroy(self, *args):
        Gtk.Window.destroy(self)

    def update_interface(self):
        # Optimization / Threads
        threads_adjustment = self._builder.get_object("threads_adjustment")
        threads_adjustment.set_value(
            self._config.getint("optimization", "threads")
        )

        # Interface / Theme
        if (
            gtk_themes_helpers.get_gtk_theme_name()
            in gtk_themes_helpers.list_gtk_themes()
        ):
            theme_combobox = self._builder.get_object("theme_combobox")
            theme_combobox.set_active(
                gtk_themes_helpers.list_gtk_themes().index(
                    gtk_themes_helpers.get_gtk_theme_name()
                )
            )

        # Interface / Prefer dark theme
        prefer_dark_theme_switch = self._builder.get_object(
            "prefer_dark_theme_switch"
        )
        prefer_dark_theme_switch.set_state(
            self._config.getboolean(
                "interface", "gtk-application-prefer-dark-theme"
            )
        )

        # Output file / Output files location
        output_pattern_radiobuttons = {
            "next-to-file": self._builder.get_object(
                "output_pattern_next_to_file_radiobutton"
            ),
            "subfolder": self._builder.get_object(
                "output_pattern_subfolder_radiobutton"
            ),
            "custom": self._builder.get_object(
                "output_pattern_custom_radiobutton"
            ),
        }
        output_pattern_radiobuttons[
            self._config.get("output", "active-pattern")
        ].set_active(True)

        output_pattern_custom_entry = self._builder.get_object(
            "output_pattern_custom_entry"
        )
        output_pattern_custom_entry.set_text(
            self._config.get("output", "custom-pattern")
        )

        output_pattern_custom_entry.set_sensitive(
            self._config.get("output", "active-pattern") == "custom"
        )

    def _prepare_theme_combobox(self):
        theme_combobox = self._builder.get_object("theme_combobox")

        for theme in gtk_themes_helpers.list_gtk_themes():
            theme_combobox.append_text(theme)

    def _on_threads_adjustment_value_changed(self, adjustment):
        self._config.set(
            "optimization", "threads", str(int(adjustment.get_value()))
        )

    def _on_theme_combobox_changed(self, widget):
        gtk_theme = gtk_themes_helpers.list_gtk_themes()[widget.get_active()]
        self._config.set("interface", "gtk-theme-name", gtk_theme)
        gtk_themes_helpers.set_gtk_theme_name(gtk_theme)

    def _on_prefer_dark_theme_switch_state_setted(self, widget, state):
        self._config.set(
            "interface", "gtk-application-prefer-dark-theme", str(state)
        )
        gtk_themes_helpers.set_gtk_application_prefer_dark_theme(state)

    def _on_output_pattern_next_to_file_radiobutton_toggled(self, widget):
        if not widget.get_active():
            return
        self._config.set("output", "active-pattern", "next-to-file")
        output_pattern_custom_entry = self._builder.get_object(
            "output_pattern_custom_entry"
        )
        output_pattern_custom_entry.set_sensitive(False)

    def _on_output_pattern_subfolder_radiobutton_toggled(self, widget):
        if not widget.get_active():
            return
        self._config.set("output", "active-pattern", "subfolder")
        output_pattern_custom_entry = self._builder.get_object(
            "output_pattern_custom_entry"
        )
        output_pattern_custom_entry.set_sensitive(False)

    def _on_output_pattern_custom_radiobutton_toggled(self, widget):
        if not widget.get_active():
            return
        self._config.set("output", "active-pattern", "custom")
        output_pattern_custom_entry = self._builder.get_object(
            "output_pattern_custom_entry"
        )
        output_pattern_custom_entry.set_sensitive(True)

    def _on_output_pattern_custom_entry_changed(self, widget):
        self._config.set("output", "custom-pattern", widget.get_text())

    def _on_settings_windows_destroyed(self, widget):
        save_config(self._config)
