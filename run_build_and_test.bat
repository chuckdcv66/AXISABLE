@echo off
title 🚀 Building CELESTIAL + Running Tests
color 0B
setlocal enabledelayedexpansion

echo.
echo [1/3] Installing requirements from offline_packages...
python -m pip install --no-index --find-links=offline_packages -r offline_packages\requirements.txt
if errorlevel 1 (
    echo ❌ Dependency installation failed.
    pause
    exit /b 1
)

echo.
echo [2/3] Running test suite...
python tests\test_voice_thread.py
if errorlevel 1 (
    echo ❌ Voice engine test failed.
    pause
    exit /b 1
)
python tests\test_memory_thread.py
if errorlevel 1 (
    echo ❌ Memory audit test failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Compiling CELESTIAL with PyInstaller...
pyinstaller CELESTIAL.spec --noconfirm --clean
if errorlevel 1 (
    echo ❌ PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo ✅ Build complete! You’ll find CELESTIAL.exe inside: dist\CELESTIAL\
pause


