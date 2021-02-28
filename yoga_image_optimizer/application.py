import os

from . import APPLICATION_ID
from .main_window import MainWindow

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf  # noqa: E402


class YogaImageOptimizerApplication(Gtk.Application):

    STATE_MANAGE_IMAGES = "manage"
    STATE_OPTIMIZE = "optimize"

    def __init__(self):
        Gtk.Application.__init__(
                self,
                application_id=APPLICATION_ID,
                flags=Gio.ApplicationFlags.HANDLES_OPEN)

        self.current_state = None
        self._main_window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action_quit = Gio.SimpleAction.new("quit", None)
        action_quit.connect("activate", self.on_quit)
        self.add_action(action_quit)

    def do_activate(self):
        if not self._main_window:
            self._main_window = MainWindow(self)
            self.switch_state(self.STATE_MANAGE_IMAGES)

        self._main_window.show()
        self._main_window.present()

    def do_open(self, files, file_count, hint):
        self.do_activate()

        if self.current_state == self.STATE_OPTIMIZE:
            # TODO display a message to inform the user we cannot add files now
            return

        for file_ in files:
            self.add_image(file_.get_path())

    def switch_state(self, state):
        self.current_state = state
        self._main_window.switch_state(state)

    def add_image(self, path):
        input_path = os.path.abspath(path)
        output_path = "".join([
                os.path.splitext(path)[0],
                ".opti",
                os.path.splitext(path)[1]])
        preview = GdkPixbuf.Pixbuf.new_from_file_at_size(input_path, 64, 64)
        self._main_window.image_store.append([
            preview,
            os.path.basename(input_path),
            "XXX",  # TODO
            "➡️",
            os.path.basename(output_path),
            "XXX",  # TODO
            "",
            input_path,
            output_path])

    def optimize(self):
        self.switch_state(self.STATE_OPTIMIZE)
        # TODO

    def stop_optimization(self):
        self.switch_state(self.STATE_MANAGE_IMAGES)
        # TODO

    def on_quit(self, action, param):
        self.quit()
