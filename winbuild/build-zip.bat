:: Get the YOGA Image Optimizer version
FOR /F %%i IN ('python setup.py --version') DO (
    SET VERSION=%%i
)

:: Output name
SET OUTPUT_NAME=yoga-image-optimizer_%VERSION%_win64

:: Create required folders
mkdir build
mkdir dist

:: Release
xcopy /E /Y yoga-image-optimizer.dist build\%OUTPUT_NAME%\
cd build
powershell Compress-Archive %OUTPUT_NAME% ..\dist\%OUTPUT_NAME%.zip
del /S /Q %OUTPUT_NAME%
cd ..
