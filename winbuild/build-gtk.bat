SET GVSBUILD_REV=2022.4.1
SET ROOTDIR=%CD%

:: Get or update gvsbuild
IF NOT EXIST build\gvsbuild (
    mkdir build
    git clone https://github.com/wingtk/gvsbuild.git build\gvsbuild
    CD build\gvsbuild
    git checkout %GVSBUILD_REV%
) ELSE (
    CD build\gvsbuild
    git checkout master
    git pull
    git checkout %GVSBUILD_REV%
)

:: Install the Python version that will be used to build
python build.py build ^
    -p x64 ^
    --vs-ver 17 ^
    python

:: build Gtk with introspection enabled and Adwaita
python build.py build ^
    -p x64 ^
    --vs-ver 17 ^
    --enable-gi ^
    gtk3 adwaita-icon-theme

::
CD %ROOTDIR%
