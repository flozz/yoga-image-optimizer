:: Get the Windows 10 GTK theme
IF NOT EXIST build\windows10 (
    mkdir build
    git clone https://github.com/B00merang-Project/Windows-10 build\windows10
)

:: Copy the GTK theme to the right folder
mkdir yoga-image-optimizer.dist\gtk\share\themes\Windows10\
xcopy /E /Y ^
    build\windows10\gtk-3.20 ^
    yoga-image-optimizer.dist\gtk\share\themes\Windows10\gtk-3.20\

:: Copy the GTK theme license files
mkdir yoga-image-optimizer.dist\gtk\share\doc\windows10-gtk-theme\
copy build\windows10\LICENSE.md ^
    yoga-image-optimizer.dist\gtk\share\doc\windows10-gtk-theme\LICENSE.md
copy build\windows10\CREDITS ^
    yoga-image-optimizer.dist\gtk\share\doc\windows10-gtk-theme\CREDITS

:: Copy the setting file to apply the theme
copy winbuild\gtk-3.0.settings.ini ^
    yoga-image-optimizer.dist\gtk\etc\gtk-3.0\settings.ini
