@echo off
cd /d "%~dp0"

echo Activating venv and launching Celestial...

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Launch the GUI
cd interface
python interface_celestial_unified.py

pause
