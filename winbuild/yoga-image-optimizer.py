#!/usr/bin/env python

import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

_paths = os.environ["PATH"].split(os.pathsep)
_paths.insert(0, str(ROOT / "gtk" / "bin"))
os.environ["PATH"] = os.pathsep.join(_paths)

os.environ["GI_TYPELIB_PATH"] = str(ROOT / "gtk" / "lib" / "girepository-1.0")
os.environ["XDG_DATA_DIRS"] = str(ROOT / "gtk" / "share")

if __name__ == "__main__":
    from yoga_image_optimizer.__main__ import main

    main()
