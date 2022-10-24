YOGA Image Optimizer - Windows Build
====================================

Requirements
------------

To build YOGA Image Optimizer for Windows, you must first install the following
dependencies:

* Windows 11:

  * Download (VM): https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/

Install Chocolatey (optional, but simpler setup):

  * Run in PowerShell as administrator:
    ``Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))``
  * NOTE: all ``choco`` commands should be run as administrator

* Python 3.10:

  * 64bit version
  * Must be added to the PATH (there is a checkbox during the installation)
  * Virtualenv must be installed and available in the PATH too
  * Download: https://www.python.org/
  * Choco: ``choco install python``

* Git:

  * Download: https://git-scm.com/
  * Choco: ``choco install git``

* MSYS2:

  * Install it at default location (``C:\msys64``)
  * Download: https://www.msys2.org/
  * Choco: ``choco install msys2``

* Visual Studio 17 (2022)

  * Already installed in the Windows 11 Dev VM, else use Chocolatey
  * Choco: ``choco install visualstudio2022-workload-vctools``

* Inno Setup

  * Install it at default location (``C:\Program Files (x86)\Inno Setup 6\\``)
    or change its path in ``build-installer.bat``
  * Download: https://jrsoftware.org/isinfo.php
  * Choco: ``choco install innosetup``

Restart to finish setup.


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
