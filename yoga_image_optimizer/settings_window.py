import os

from gi.repository import Gtk, GdkPixbuf

from . import APPLICATION_NAME, APPLICATION_ID
from . import data_helpers
from . import gtk_themes_helpers
from .translation import gtk_builder_translation_hack
from .translation import gettext as _
from .config import save_config


class SettingsWindow(Gtk.Window):
    def __init__(self, config):
        Gtk.Window.__init__(
            self,
            title="%s - %s" % (_("Settings"), APPLICATION_NAME),
            icon=GdkPixbuf.Pixbuf.new_from_file(
                data_helpers.find_data_path("images/icon_64.png")
            ),
            resizable=False,
        )

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

    def _on_settings_windows_destroyed(self, widget):
        save_config(self._config)
