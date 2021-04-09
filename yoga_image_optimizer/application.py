import os
import concurrent.futures
from pathlib import Path

import yoga.image
from gi.repository import Gtk, GLib, Gio

from . import APPLICATION_ID
from . import helpers
from .main_window import MainWindow
from .about_dialog import AboutDialog
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

        # Action: app.about
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", lambda a, p: self.about())
        self.add_action(action)

        # Action: app.quit
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", lambda a, p: self.quit())
        self.add_action(action)
        self.set_accels_for_action("app.quit", ["<Ctrl>q"])

        # Action: app.optimize
        action = Gio.SimpleAction.new("optimize", None)
        action.connect("activate", lambda a, p: self.optimize())
        self.add_action(action)

        # Action: app.stop-optimization
        action = Gio.SimpleAction.new("stop-optimization", None)
        action.connect("activate", lambda a, p: self.stop_optimization())
        self.add_action(action)

        # Action: app.add-image
        action = Gio.SimpleAction.new("add-image", GLib.VariantType("s"))
        action.connect("activate", lambda a, p: self.add_image(p.get_string()))
        self.add_action(action)

        # Action: app.clear-images
        action = Gio.SimpleAction.new("clear-images", None)
        action.connect("activate", lambda a, p: self.clear_images())
        self.add_action(action)

        # Action: app.open-file
        action = Gio.SimpleAction.new("open-file", None)
        action.connect("activate", lambda a, p: self.open_file())
        self.add_action(action)
        self.set_accels_for_action("app.open-file", ["<Ctrl>o"])

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

    def about(self):
        about_dialog = AboutDialog(parent=self._main_window)
        about_dialog.run()
        about_dialog.destroy()

    def quit(self):
        self.stop_optimization()
        Gtk.Application.quit(self)

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

    def clear_images(self):
        self.image_store.clear()

    def open_file(self):
        file_chooser_dialog = Gtk.FileChooserDialog(
            title="Open Images...",
            parent=self._main_window,
        )
        file_chooser_dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        file_chooser_dialog.set_select_multiple(True)

        image_file_filter = Gtk.FileFilter()
        image_file_filter.set_name("Image Files")
        image_file_filter.add_mime_type("image/jpeg")
        image_file_filter.add_mime_type("image/png")
        file_chooser_dialog.add_filter(image_file_filter)

        any_file_filter = Gtk.FileFilter()
        any_file_filter.set_name("All Files")
        any_file_filter.add_pattern("*")
        file_chooser_dialog.add_filter(any_file_filter)

        response = file_chooser_dialog.run()

        if response == Gtk.ResponseType.OK:
            for filename in file_chooser_dialog.get_filenames():
                self.add_image(filename)

        file_chooser_dialog.destroy()

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
