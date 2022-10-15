SET GVSBUILD_REV=3562dd1de6817acf76f641d148f2c3ad0580407a
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

:: Install the Python version that will be used to build...
python build.py build ^
    -p x64 ^
    --vs-ver 17 ^
    python

:: ... and patch it to allow our build to work
COPY %ROOTDIR%\winbuild\patch\cygwinccompiler.py ^
     C:\gtk-build\tools\python.3.9.2\tools\lib\distutils\cygwinccompiler.py

:: build Gtk with introspection enabled and Adwaita
python build.py build ^
    -p x64 ^
    --vs-ver 17 ^
    --enable-gi ^
    gtk3 adwaita-icon-theme

::
CD %ROOTDIR%
