import locale
import gettext

from . import APPLICATION_ID
from . import data_helpers

locale.bindtextdomain(APPLICATION_ID, data_helpers.find_data_path("locales"))
translation = gettext.translation(
    APPLICATION_ID, localedir=data_helpers.find_data_path("locales")
)
gettext = translation.gettext
