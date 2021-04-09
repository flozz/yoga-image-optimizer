from . import APPLICATION_NAME
from . import VERSION
from . import helpers

from gi.repository import Gtk, GdkPixbuf


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent=None):
        Gtk.AboutDialog.__init__(
            self,
            parent=parent,
            program_name=APPLICATION_NAME,
            comments="A graphical interface to optimizes JPEG and PNG images (based on YOGA)",
            version=VERSION,
            copyright="Copyright (c) 2021 Fabien LOISON",
            website_label="github.com/flozz/yoga-image-optimizer",
            website="https://github.com/flozz/yoga-image-optimizer",
            license_type=Gtk.License.GPL_3_0,
        )

        logo = GdkPixbuf.Pixbuf.new_from_file(
            helpers.find_data_path("images/logo.svg")
        )
        self.set_logo(logo)
