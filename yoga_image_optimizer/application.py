import os
import concurrent.futures
from pathlib import Path

import yoga.image
from gi.repository import Gtk, GLib, Gio

from . import APPLICATION_ID
from . import helpers
from .main_window import MainWindow
from .image_store import ImageStore


_IMAGE_FORMATS = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
}


class YogaImageOptimizerApplication(Gtk.Application):

    STATE_MANAGE_IMAGES = "manage"
    STATE_OPTIMIZE = "optimize"

    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
        )

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
        input_path = Path(path).resolve()
        input_size = input_path.stat().st_size
        ext = input_path.suffix.lower()

        self.image_store.append(
            input_file=input_path.as_posix(),
            output_file=helpers.add_suffix_to_filename(input_path.as_posix()),
            input_size=input_size,
            output_size=0,
            input_format=_IMAGE_FORMATS[ext],
            output_format=_IMAGE_FORMATS[ext],
            preview=helpers.preview_gdk_pixbuf_from_path(
                input_path.as_posix()
            ),
        )

    def remove_selected_image(self):
        treeview_images = self._main_window.get_images_treeview()
        selection = treeview_images.get_selection()

        if selection.count_selected_rows() == 0:
            return

        _, iter_ = selection.get_selected()
        self.image_store.remove(iter_)

    def optimize(self):
        self.switch_state(self.STATE_OPTIMIZE)

        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self._futures = []

        for row in self.image_store.get_all():
            self._futures.append(
                self._executor.submit(
                    yoga.image.optimize,
                    row["input_file"],
                    row["output_file"],
                    {
                        "output_format": row["output_format"].lower(),
                        "jpeg_quality": row["jpeg_quality"] / 100,
                    },
                )
            )

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
                    status=self.image_store.STATUS_IN_PROGRESS,
                    output_size=0,
                )
                is_running = True
            elif future.done():
                image_data = self.image_store.get(i)
                output_size = os.stat(image_data["output_file"]).st_size

                self.image_store.update(
                    i,
                    status=self.image_store.STATUS_DONE,
                    output_size=output_size,
                )
            else:
                self.image_store.update(
                    i,
                    status=self.image_store.STATUS_PENDING,
                    output_size=0,
                )

        if is_running:
            GLib.timeout_add_seconds(0.1, self._update_optimization_status)
        else:
            self.stop_optimization()
