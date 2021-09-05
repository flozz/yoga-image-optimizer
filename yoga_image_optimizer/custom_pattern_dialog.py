import os

from gi.repository import Gtk

from . import APPLICATION_ID
from . import data_helpers
from .translation import gtk_builder_translation_hack


class CustomPatternDialog(object):
    def __init__(self, initial_pattern="", parent_window=None):
        self._custom_pattern = None

        self._builder = Gtk.Builder()
        self._builder.set_translation_domain(APPLICATION_ID)
        self._builder.add_from_file(
            data_helpers.find_data_path("ui/custom-pattern-dialog.glade")
        )
        self._builder.connect_signals(self)

        self._dialog = self._builder.get_object("custom_pattern_dialog")
        self._entry = self._builder.get_object("custom_pattern_entry")
        self._entry.set_text(initial_pattern)

        self._dialog.set_transient_for(parent_window)

        # HACK: Translate the UI on Windows
        if os.name == "nt":
            gtk_builder_translation_hack(self._builder)

    def run(self):
        self._dialog.run()
        return self._custom_pattern

    def _on_cancel_button_cliqued(self, widget):
        self._dialog.destroy()

    def _on_apply_button_cliqued(self, widget):
        self._custom_pattern = self._entry.get_text()
        self._dialog.destroy()

    def _on_custom_pattern_dialog_response(self, widget, response_id):
        self._dialog.destroy()
