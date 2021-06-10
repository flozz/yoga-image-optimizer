from gi.repository import Gtk
from gi.repository import GdkPixbuf

from . import APPLICATION_NAME
from . import VERSION
from . import data_helpers
from .translation import gettext as _


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent=None):
        Gtk.AboutDialog.__init__(
            self,
            parent=parent,
            program_name=APPLICATION_NAME,
            comments=_(
                "A graphical interface to convert and optimize "
                "JPEG, PNG and WebP images (based on YOGA)"
            ),
            version=VERSION,
            copyright="Copyright (c) 2021 Fabien LOISON",
            website_label="yoga.flozz.org",
            website="https://yoga.flozz.org/",
            license_type=Gtk.License.GPL_3_0,
        )

        logo = GdkPixbuf.Pixbuf.new_from_file(
            data_helpers.find_data_path("images/icon_256.png")
        )
        self.set_logo(logo)

        self.set_artists(
            [
                "Katia ROBINSON (Wanadev)",
            ]
        )

        self.set_translator_credits(_("translator-credits"))
