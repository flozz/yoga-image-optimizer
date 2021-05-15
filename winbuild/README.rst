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


Building YOGA Image Optimizer for Windows
-----------------------------------------

All commands must be run from the project's root directory (the one that
contains the ``setup.py`` file).

1. Build GTK by running ``winbuild\build-gtk.bat`` using cmd.exe,
