import os
import concurrent.futures
import threading

import yoga.image

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

        self._executor = None
        self._futures = []

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

        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self._futures = []

        for row in self._main_window.image_store:
            input_path = row[7]
            output_path = row[8]
            self._futures.append(self._executor.submit(
                yoga.image.optimize,
                input_path,
                output_path))

        self._update_optimization_status()

    def stop_optimization(self):
        if self.current_state != self.STATE_OPTIMIZE:
            return

        self._executor.shutdown(wait=False)
        for future in self._futures:
            future.cancel()

        self.switch_state(self.STATE_MANAGE_IMAGES)

    def on_quit(self, action, param):
        self.stop_optimization()
        self.quit()

    def _update_optimization_status(self):
        if self.current_state != self.STATE_OPTIMIZE:
            return

        image_store = self._main_window.image_store
        is_running = False

        for i in range(len(self._futures)):
            future = self._futures[i]

            if future.running():
                image_store[i][6] = "🔄️ Optimizing..."
                is_running = True
            elif future.done():
                image_store[i][6] = "✅️ Done"
            else:
                image_store[i][6] = "⏸️ Pending"

        if is_running:
            timer = threading.Timer(0.1, self._update_optimization_status)
            timer.start()
        else:
            self.stop_optimization()
