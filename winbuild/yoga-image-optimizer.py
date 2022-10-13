#!/usr/bin/env python

import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

_paths = os.environ["PATH"].split(os.pathsep)
_paths.insert(0, str(ROOT / "gtk" / "bin"))
os.environ["PATH"] = os.pathsep.join(_paths)

os.environ["GI_TYPELIB_PATH"] = str(ROOT / "gtk" / "lib" / "girepository-1.0")
os.environ["XDG_DATA_DIRS"] = str(ROOT / "gtk" / "share")

import gi.overrides.Gtk  # noqa: F401, E402
import gi.overrides.GLib  # noqa: F401, E402
import gi.overrides.GObject  # noqa: F401, E402

# From gi.overrides.Gdk (importing it do not work...)
from gi.repository import Gdk  # noqa: E402

Gdk.EventType._2BUTTON_PRESS = getattr(Gdk.EventType, "2BUTTON_PRESS")

if __name__ == "__main__":
    from yoga_image_optimizer.__main__ import main

    main()
