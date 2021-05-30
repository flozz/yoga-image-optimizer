SET GVSBUILD_REV=9b10978a8c5aa539f4280feeaa69bc5cc8bf9fbf
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
    --vs-ver 16 ^
    python

:: ... and patch it to allow our build to work
COPY %ROOTDIR%\winbuild\patch\cygwinccompiler.py ^
     C:\gtk-build\tools\python.3.9.2\tools\lib\distutils\cygwinccompiler.py

:: build Gtk with introspection enabled and Adwaita
python build.py build ^
    -p x64 ^
    --vs-ver 16 ^
    --enable-gi ^
    gtk3 adwaita-icon-theme

::
CD %ROOTDIR%
