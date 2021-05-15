import locale
import gettext

from . import APPLICATION_ID
from . import data_helpers


translation = gettext.translation(
    APPLICATION_ID,
    localedir=data_helpers.find_data_path("locales"),
    fallback=True,
)

gettext = translation.gettext
format_string = locale.format_string
