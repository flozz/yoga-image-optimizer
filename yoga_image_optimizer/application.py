import os
import concurrent.futures

import yoga.image

from . import APPLICATION_ID
from . import helpers
from .main_window import MainWindow
from .image_store import ImageStore

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gio, GdkPixbuf  # noqa: E402


class YogaImageOptimizerApplication(Gtk.Application):

    STATE_MANAGE_IMAGES = "manage"
    STATE_OPTIMIZE = "optimize"

    STATUS_NONE = 0
    STATUS_PENDING = 1
    STATUS_IN_PROGRESS = 2
    STATUS_DONE = 3

    def __init__(self):
        Gtk.Application.__init__(
                self,
                application_id=APPLICATION_ID,
                flags=Gio.ApplicationFlags.HANDLES_OPEN)

        self.current_state = None
        self.image_store = ImageStore()

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
                os.path.splitext(input_path)[0],
                ".opti",
                os.path.splitext(input_path)[1]])
        output_path_display = os.path.relpath(
                output_path, start=os.path.dirname(input_path))
        preview = GdkPixbuf.Pixbuf.new_from_file_at_size(input_path, 64, 64)
        input_size = os.stat(input_path).st_size

        data = {
            "input_file": input_path,
            "output_file": output_path,
            "input_file_display": os.path.basename(input_path),
            "output_file_display": output_path_display,
            "input_size": input_size,
            "output_size": 0,
            "input_size_display": helpers.human_readable_file_size(input_size),
            "output_size_display": "",
            "input_format": "",  # TODO
            "output_format": "",  # TODO
            "output_format_display": "",  # TODO
            "preview": preview,
            "separator": "➡️",
            "status": 0,
            "status_display": "",
        }

        self.image_store.append(**data)

    def optimize(self):
        self.switch_state(self.STATE_OPTIMIZE)

        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self._futures = []

        for row in self.image_store.get_all():
            self._futures.append(self._executor.submit(
                yoga.image.optimize,
                row["input_file"],
                row["output_file"]))

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

        is_running = False

        for i in range(len(self._futures)):
            future = self._futures[i]

            if future.running():
                self.image_store.update(
                        i,
                        status=self.STATUS_IN_PROGRESS,
                        status_display="🔄️ In progress",
                        output_size=0,
                        output_size_display="")
                is_running = True
            elif future.done():
                image_data = self.image_store.get(i)

                input_size = image_data["input_size"]
                output_size = os.stat(image_data["output_file"]).st_size

                size_delta = 100 - min(input_size, output_size) / max(input_size, output_size) * 100  # noqa: E501

                output_size_display = "%s (%s%.1f %%)" % (
                    helpers.human_readable_file_size(output_size),
                    "-" if output_size <= output_size else "+",
                    size_delta,
                )

                self.image_store.update(
                        i,
                        status=self.STATUS_DONE,
                        status_display="✅️ Done",
                        output_size=output_size,
                        output_size_display=output_size_display)
            else:
                self.image_store.update(
                        i,
                        status=self.STATUS_PENDING,
                        status_display="⏸️ Pending",
                        output_size=0,
                        output_size_display="")

        if is_running:
            GLib.timeout_add_seconds(0.1, self._update_optimization_status)
        else:
            self.stop_optimization()
