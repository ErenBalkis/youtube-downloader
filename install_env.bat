@echo off
:: ============================================================
::  YouTube Downloader - Environment Setup
::  Run this ONCE to create a virtual environment and install
::  all dependencies. Safe to re-run anytime.
:: ============================================================
title YouTube Downloader - Setup
cd /d "%~dp0"

echo.
echo  ====================================
echo    YouTube Downloader - Setup
echo  ====================================
echo.

:: ----------------------------------------------------------
:: 1. Check Python installation
:: ----------------------------------------------------------
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo  [ERROR] Python was not found on your system.
    echo  Please install Python 3.10+ from https://python.org
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo  [OK] Found %PYVER%
echo.

:: ----------------------------------------------------------
:: 2. Create virtual environment if it doesn't exist
:: ----------------------------------------------------------
if not exist "%~dp0venv\Scripts\activate.bat" (
    echo  [*] Creating virtual environment...
    python -m venv "%~dp0venv"
    if %errorlevel% neq 0 (
        echo  [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo  [OK] Virtual environment created.
) else (
    echo  [OK] Virtual environment already exists.
)
echo.

:: ----------------------------------------------------------
:: 3. Activate the virtual environment
:: ----------------------------------------------------------
echo  [*] Activating virtual environment...
call "%~dp0venv\Scripts\activate.bat"

:: ----------------------------------------------------------
:: 4. Upgrade pip and install dependencies
:: ----------------------------------------------------------
echo  [*] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo  [OK] pip upgraded.
echo.

echo  [*] Installing dependencies from requirements.txt...
pip install -r "%~dp0requirements.txt" --quiet
if %errorlevel% neq 0 (
    echo  [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo  [OK] All dependencies installed.
echo.

:: ----------------------------------------------------------
:: 5. Done
:: ----------------------------------------------------------
echo  ====================================
echo    Setup Complete!
echo    You can now use the app.
echo    Double-click "run_app.bat" to start.
echo  ====================================
echo.
pause
