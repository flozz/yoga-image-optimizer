import os
from pathlib import Path
import ctypes
from configparser import ConfigParser

from . import APPLICATION_ID


OUTPUT_PATTERN_NEXT_TO_FILE = "next-to-file"
OUTPUT_PATTERN_SUBFOLDER = "subfolder"
OUTPUT_PATTERN_CUSTOM = "custom"
DEFAULT_OUTPUT_PATTERNS = {
    "next-to-file": "{FILENAME}.opti.{EXT}",
    "subfolder": "optimized/{FILENAME}.{EXT}",
}

DEFAULT = {
    "optimization": {
        "threads": 2,
    },
    "interface": {
        "gtk-theme-name": "default",
        "gtk-application-prefer-dark-theme": False,
    },
    "output": {
        "active-pattern": OUTPUT_PATTERN_NEXT_TO_FILE,
        "custom-pattern": "optimized/{EXT}/example_{FILENAME}.{EXT}",
    },
}


def get_unix_xdg_config_home():
    """Returns the path to the user's config directory (XDG_CONFIG_HOME) on
    Unix platforms.

    :rtype: pathlib.Path
    """
    if "XDG_CONFIG_HOME" in os.environ and os.environ["XDG_CONFIG_HOME"]:
        config_dir = Path(os.environ["XDG_CONFIG_HOME"])
    else:
        config_dir = Path("~/.config")
    return config_dir.expanduser().resolve().absolute()


def get_win_user_data_dir():
    """Returns the user's data path on Windows platform.

    :rtype: pathlib.Path
    """
    if "APPDATA" in os.environ and os.environ["APPDATA"]:
        user_data_dir = Path(os.environ["APPDATA"])
    else:
        CSIDL_APPDATA = 26
        MAX_PATH = 2048

        buff = ctypes.create_unicode_buffer(MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(
            None, CSIDL_APPDATA, None, 0, buff
        )

        buff2 = ctypes.create_unicode_buffer(MAX_PATH)
        ctypes.windll.kernel32.GetShortPathNameW(buff.value, buff2, MAX_PATH)

        user_data_dir = Path(buff2.value)

    return user_data_dir.expanduser().resolve().absolute()


def get_config_file_path():
    """Returns the path to the application's config file.

    :rtype: pathlib.Path
    """
    if os.name == "posix":
        return get_unix_xdg_config_home() / APPLICATION_ID / "config.ini"
    elif os.name == "nt":
        return get_win_user_data_dir() / APPLICATION_ID / "config.ini"


def get_config():
    """Get the application configuration.

    :rtype: configparser.ConfigParser
    """
    config = ConfigParser()

    # Load defaults
    config.read_dict(DEFAULT)

    # Load user configuration
    config_path = get_config_file_path()
    if config_path.exists():
        config.read(config_path)

    return config


def save_config(config):
    """Save the given configuration.

    :param configparser.ConfigParser config: The configuration to save.
    """
    config_path = get_config_file_path()

    if not config_path.parent.exists():
        config_path.parent.mkdir(parents=True)

    with open(config_path, "w") as config_file:
        config.write(config_file)
