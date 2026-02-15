@echo off
:: ============================================================
::  YouTube Downloader - Launcher
::  Double-click this file to start the application.
::  A browser tab will open automatically.
:: ============================================================
title YouTube Downloader
cd /d "%~dp0"

:: ----------------------------------------------------------
:: 1. Check that venv exists
:: ----------------------------------------------------------
if not exist "%~dp0venv\Scripts\activate.bat" (
    echo.
    echo  [ERROR] Virtual environment not found!
    echo  Please run "install_env.bat" first.
    echo.
    pause
    exit /b 1
)

:: ----------------------------------------------------------
:: 2. Activate the virtual environment
:: ----------------------------------------------------------
call "%~dp0venv\Scripts\activate.bat"

:: ----------------------------------------------------------
:: 3. Launch Streamlit (browser opens automatically)
:: ----------------------------------------------------------
echo.
echo  ====================================
echo    YouTube Downloader
echo    Starting the application...
echo    Close this window to stop the app.
echo  ====================================
echo.

streamlit run "%~dp0app.py" --server.headless false --browser.gatherUsageStats false
