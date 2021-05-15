:: Path to the Inno Setup compiler
SET ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

:: Get the YOGA Image Optimizer version
FOR /F %%i IN ('python setup.py --version') DO (
    SET VERSION=%%i
)

:: Build the installer using Inno Setup
%ISCC% ^
    /DMyAppVersion=%VERSION% ^
    winbuild\windows-installer.iss

:: Move the result to the dist/ folder
mkdir dist
move winbuild\Output\*.exe dist\
