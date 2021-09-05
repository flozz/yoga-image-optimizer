YOGA Image Optimizer - Windows Build
====================================

Requirements
------------

To build YOGA Image Optimizer for Windows, you must first install the following
dependencies:

* Python 3.9:

  * 64bit version
  * Must be added to the PATH (there is a checkbox during the installation)
  * Virtualenv must be installed and available in the PATH too
  * Download: https://www.python.org/

* MSYS2:

  * Install it at default location (``C:\msys64``)
  * Download: https://www.msys2.org/

* Git:

  * Download: https://git-scm.com/

* Visual Studio 16 (2019)

* Inno Setup

  * Install it at default location (``C:\Program Files (x86)\Inno Setup 6\\``)
    or change its path in ``build-installer.bat``
  * Download: https://jrsoftware.org/isinfo.php


Building YOGA Image Optimizer for Windows
-----------------------------------------

All commands must be run from the project's root directory (the one that
contains the ``setup.py`` file).

1. Build GTK by running ``winbuild\build-gtk.bat`` using cmd.exe,
2. Build YOGA Image Optimizer running ``winbuild\build-yoga.bat`` using
   cmd.exe,
3. Add the Windows 10 GTK theme running ``winbuild\add-gtk-theme.bat`` using
   cmd.exe (optional),
4. Clean GTK build (441 Mo -> 40 Mo) running ``winbuild/clean-gtk.sh`` using
   Git Bash or MSYS2,


Building distribuable files
---------------------------

* Windows installer: run ``winbuild\build-installer.bat``
* Zip: run ``winbuild\build-zip.bat``

Results goes to the ``dist``  folder.
