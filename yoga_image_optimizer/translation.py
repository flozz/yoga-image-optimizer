import os
import locale
import gettext

from . import APPLICATION_ID
from . import data_helpers


if "LANG" not in os.environ:
    language, encoding = locale.getlocale()
    os.environ["LANG"] = language

translation = gettext.translation(
    APPLICATION_ID,
    localedir=data_helpers.find_data_path("locales"),
    fallback=True,
)

if hasattr(locale, "bindtextdomain"):
    locale.bindtextdomain(
        APPLICATION_ID, data_helpers.find_data_path("locales")
    )
else:
    print("W: Unable to bind text domaine")

gettext = translation.gettext
format_string = locale.format_string


def gtk_builder_translation_hack(builder):
    """Hack to allow translating the UI on Windows.

    :param Gtk.Builder builder: The builder to hack...
    """
    translatable_properties = [
        "label",
        "text",
        "title",
        "tooltip-text",
    ]
    for widget in builder.get_objects():
        widget_properties = [prop.name for prop in widget.list_properties()]
        for translatable_property in translatable_properties:
            if translatable_property not in widget_properties:
                continue
            text = widget.get_property(translatable_property)
            if not text:
                continue
            widget.set_property(translatable_property, gettext(text))
