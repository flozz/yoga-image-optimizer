:: Make and/or activate the virtualenv
IF NOT EXIST build\__env__ (
    mkdir build
    python -m venv build\__env__
)
CALL build\__env__\Scripts\activate.bat

:: Set some environment varialbes for the PyGObject compilation
SET INCLUDE=^
C:\gtk-build\gtk\x64\release\include;^
C:\gtk-build\gtk\x64\release\include\glib-2.0;^
C:\gtk-build\gtk\x64\release\lib\glib-2.0\include;^
C:\gtk-build\gtk\x64\release\include\gobject-introspection-1.0;^
C:\gtk-build\gtk\x64\release\include\cairo

SET LIB=^
C:\gtk-build\gtk\x64\release\lib\

:: Adds Gtk build to the PATH to have gettext tools
PATH=^
C:\gtk-build\gtk\x64\release\bin;^
%PATH%

:: Install compilation tools (Nuitka,...)
pip install -r winbuild\requirements.txt

:: Compile locales
nox -s locales_compile

:: Install Python dependencies. This will also compile PyGObject
pip install .

:: Compile with nuitka
python -m nuitka ^
    --follow-imports ^
    --assume-yes-for-downloads ^
    --include-package=PIL ^
    --include-package-data=yoga_image_optimizer ^
    --windows-disable-console ^
    --windows-force-stderr-spec=yoga-image-optimizer.err.txt ^
    --standalone ^
    winbuild\yoga-image-optimizer.py

:: Add license,...
copy COPYING yoga-image-optimizer.dist\COPYING.txt

:: Copy GTK build
xcopy /E /Y C:\gtk-build\gtk\x64\release yoga-image-optimizer.dist\gtk\

:: Leave the virtualenv
deactivate
