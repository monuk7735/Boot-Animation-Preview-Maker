:: Don't Edit This File Unless You Know What You are Doing
@echo OFF


CALL :HEADER_TEXT

echo.Checking Files

set input_file_path = "input\"
set output_file_path = "output\"

if not exist "output\" mkdir "output\"
if not exist "input\bootanimation\" mkdir "input\bootanimation\"

:SHOW_MENU
cls
CALL :HEADER_TEXT
echo.1. Create Bootanimation Preview (for input\bootanimation\ or input\bootanimation.zip)
echo.2. Create bootanimation.zip (from input\bootanimation\)
echo.3. Exit
echo.&echo.&set /P INPUT=Choose any Option():

if /I "%INPUT%" == "1" bin\python\Scripts\python.exe bin/create_preview.py & pause
if /I "%INPUT%" == "2" bin\python\Scripts\python.exe bin/create_bootanimation.py & pause
if /I "%INPUT%" == "3" pause & EXIT

goto :SHOW_MENU

:HEADER_TEXT 
echo. ====================================================================================
echo.
echo.                           Boot Animation Preview Creator
echo.
echo.                                    by monuk7735      
echo.
echo.
echo. ====================================================================================
echo.
echo.
EXIT /B 0