from . import APPLICATION_ID
from .main_window import MainWindow

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio  # noqa: E402


class YogaImageOptimizerApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(
                self,
                application_id=APPLICATION_ID,
                flags=Gio.ApplicationFlags.FLAGS_NONE)
        self._mainWindow = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action_quit = Gio.SimpleAction.new("quit", None)
        action_quit.connect("activate", self.on_quit)
        self.add_action(action_quit)

    def do_activate(self):
        if not self._mainWindow:
            self._mainWindow = MainWindow(self)

        self._mainWindow.show()
        self._mainWindow.present()

    def on_quit(self, action, param):
        self.quit()
