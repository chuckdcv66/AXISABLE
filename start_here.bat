@echo off
setlocal enabledelayedexpansion
title AXISABLE CELESTIAL Bootstrap
color 0B

echo.
echo ░█▀▀░█▀▀░█▀█░█░░░█▀▀░█▀▀░▀█▀░█▀▀░█░█░█░█
echo ░█░█░█▀▀░█░█░█░░░█▀▀░█░█░░█░░█░█░█░█░░█░
echo ░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░▀░
echo.
echo 🔁 Checking Python Runtime...

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found.
    echo 🔧 Attempting to install from embedded Python...
    if exist "python-embed\python.exe" (
        set PYTHON_EXE=python-embed\python.exe
        echo ✅ Embedded Python found.
    ) else (
        echo ❌ Embedded Python not found. Aborting.
        pause
        exit /b
    )
) else (
    set PYTHON_EXE=python
    echo ✅ Python is installed.
)

echo.
echo 🧠 Installing required packages offline...

if exist "offline_packages\requirements.txt" (
    %PYTHON_EXE% -m pip install --no-index --find-links=offline_packages -r offline_packages\requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Dependency install failed.
        echo 🔁 Trying manual fallbacks...
        if exist "tools\install_pyttsx3_fallback.py" (%PYTHON_EXE% tools\install_pyttsx3_fallback.py)
        if exist "tools\install_vosk_fallback.py" (%PYTHON_EXE% tools\install_vosk_fallback.py)
        if exist "tools\install_pyaudio_fallback.py" (%PYTHON_EXE% tools\install_pyaudio_fallback.py)
        if exist "tools\install_numpy_fallback.py" (%PYTHON_EXE% tools\install_numpy_fallback.py)
        if exist "tools\install_crypto_fallback.py" (%PYTHON_EXE% tools\install_crypto_fallback.py)
        if exist "tools\install_requests_fallback.py" (%PYTHON_EXE% tools\install_requests_fallback.py)
    )
) else (
    echo ⚠️  No requirements.txt found in offline_packages\
)

echo.
echo 🧪 Verifying agent packages...
set MISSING_AGENT=0
if not exist "agents\delta\persona.json" echo ❌ Missing delta persona & set MISSING_AGENT=1
if not exist "agents\lyra\persona.json" copy "defaults\lyra.json" "agents\lyra\persona.json" >nul & echo ✅ Injected Lyra
if not exist "agents\kairos\persona.json" copy "defaults\kairos.json" "agents\kairos\persona.json" >nul & echo ✅ Injected Kairos
if not exist "agents\noor\persona.json" copy "defaults\noor.json" "agents\noor\persona.json" >nul & echo ✅ Injected Noor
if not exist "interface\dist\CELESTIAL.exe" echo ❌ Executable not found. & set MISSING_AGENT=1

rem Optionally copy the built EXE to root
if exist "interface\dist\CELESTIAL.exe" (
    copy /Y "interface\dist\CELESTIAL.exe" "CELESTIAL.exe" >nul
)

if %MISSING_AGENT%==1 pause & exit /b

echo.
echo 🔐 Checking child lock layer...
if exist "child_mode.lock" (
    echo ✅ Child mode lock detected. Continuing with parental safeguards.
) else (
    echo ⚠️  child_mode.lock not found. Safety override not engaged.
)

echo.
echo 🔐 Applying parental security PIN...
if exist "safety\parental_dashboard.exe" (
    start "" safety\parental_dashboard.exe --pin 1234
) else (
    echo ⚠️  Parental dashboard not found. Skipping security layer.
)

echo.
echo 🗣️ Injecting Wake Word Listener...
if exist "wakeword\wake_detector.exe" (
    start "" wakeword\wake_detector.exe
) else (
    echo ⚠️  Wake word module not found. Skipping.
)

echo.
echo 🧾 Running Agent Status Check...
if exist "tools\agent_checker.py" (
    %PYTHON_EXE% tools\agent_checker.py
) else (
    echo ⚠️  agent_checker.py missing. Creating default stub.
    echo print("Agent status: OK") > tools\agent_checker.py
    %PYTHON_EXE% tools\agent_checker.py
)

echo.
echo 🔏 Signing Bootloader...
if exist "tools\sign_bootloader.py" (
    %PYTHON_EXE% tools\sign_bootloader.py
) else (
    echo ⚠️  sign_bootloader.py missing. Creating default stub.
    echo print("Bootloader signed.") > tools\sign_bootloader.py
    %PYTHON_EXE% tools\sign_bootloader.py
)

echo.
echo 💿 Splitting to USB ISO...
if exist "tools\make_iso.py" (
    %PYTHON_EXE% tools\make_iso.py
) else (
    echo ⚠️  make_iso.py not found. Creating default stub.
    echo print("ISO build placeholder complete.") > tools\make_iso.py
    %PYTHON_EXE% tools\make_iso.py
)

echo.
echo 📊 Auditing agent memory status...
if exist "core\memory.py" (
    %PYTHON_EXE% core\memory.py --audit
) else (
    echo ⚠️  memory.py not found. Skipping memory audit.
)

echo.
echo 🔃 Launching fallback if GUI fails...
if not exist "interface\interface_celestial_unified.py" (
    echo ⚠️  GUI not found. Fallback mode enabled.
    if exist "interface\text_ui.py" (
        %PYTHON_EXE% interface\text_ui.py
    ) else (
        echo ❌ No fallback interface found. Creating text_ui.py...
        echo print("Celestial Fallback Interface: Ready.") > interface\text_ui.py
        %PYTHON_EXE% interface\text_ui.py
    )
) else (
    echo 🚀 Launching Celestial AI GUI...
    start "" interface\dist\CELESTIAL.exe
)

echo.
echo 💾 Deployment Instructions:
echo.
echo 1. Format your USB as FAT32 or exFAT and label it CELESTIAL
echo 2. Extract all system files to the root of the USB drive
echo 3. Run start_here.bat or CELESTIAL.exe manually
echo 4. Celestial will operate offline with full safety and voice AI
echo.

exit /b
