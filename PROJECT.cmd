@echo off
setlocal enabledelayedexpansion
title HYPOCRITICAL SAINT CLI

:: Normalize first argument
set "CMD_ARG=%~1"
if /i "%CMD_ARG%"=="RUN" goto :do_run
if /i "%CMD_ARG%"=="START" goto :do_run
if /i "%CMD_ARG%"=="STATUS" goto :do_status
if /i "%CMD_ARG%"=="HELP" goto :do_help
if "%CMD_ARG%"=="" goto :do_help

echo [ERROR] Unknown argument: %CMD_ARG%
echo.
goto :do_help

:do_help
echo ==============================================================================
echo                          HYPOCRITICAL SAINT
echo                  Digital Image Steganography Studio
echo            "Innocent on the Outside. Secret on the Inside."
echo ==============================================================================
echo.
echo Usage:
echo   PROJECT RUN       - Start the studio server and open in default browser
echo   PROJECT STATUS    - Check if the local studio server is running
echo   PROJECT HELP      - Show this help message
echo.
echo Project Home: https://github.com/xdc7-css/Hypocritical-Saint
echo Local Web UI: http://127.0.0.1:7860
echo ==============================================================================
exit /b 0

:do_status
echo [*] Checking HYPOCRITICAL SAINT server status...
netstat -ano | findstr ":7860" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] HYPOCRITICAL SAINT is currently RUNNING at http://127.0.0.1:7860
) else (
    echo [INFO] HYPOCRITICAL SAINT is NOT running. Start it with: PROJECT RUN
)
exit /b 0

:do_run
:: Locate project installation directory
set "FOUND_DIR="
if defined HYPOCRITICAL_SAINT_HOME if exist "%HYPOCRITICAL_SAINT_HOME%\app.py" set "FOUND_DIR=%HYPOCRITICAL_SAINT_HOME%"
if not defined FOUND_DIR if defined HYPOCRITICAL_SAINT_DIR if exist "%HYPOCRITICAL_SAINT_DIR%\app.py" set "FOUND_DIR=%HYPOCRITICAL_SAINT_DIR%"
if not defined FOUND_DIR if exist "%~dp0app.py" set "FOUND_DIR=%~dp0"
if not defined FOUND_DIR if exist "D:\Hypocritical-Saint\app.py" set "FOUND_DIR=D:\Hypocritical-Saint"
if not defined FOUND_DIR if exist "C:\Hypocritical-Saint\app.py" set "FOUND_DIR=C:\Hypocritical-Saint"
if not defined FOUND_DIR if exist "%USERPROFILE%\Hypocritical-Saint\app.py" set "FOUND_DIR=%USERPROFILE%\Hypocritical-Saint"
if not defined FOUND_DIR if exist "X:\Stegano-master\app.py" set "FOUND_DIR=X:\Stegano-master"

if not defined FOUND_DIR (
    echo [ERROR] HYPOCRITICAL SAINT installation could not be found!
    echo Looked in:
    echo   - %~dp0
    echo   - D:\Hypocritical-Saint
    echo   - C:\Hypocritical-Saint
    echo   - %USERPROFILE%\Hypocritical-Saint
    echo.
    echo Please run setup.ps1 first to install the application.
    pause
    exit /b 1
)

:: Check if already running on port 7860
netstat -ano | findstr ":7860" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] HYPOCRITICAL SAINT is already running at http://127.0.0.1:7860
    echo [*] Opening default web browser...
    start http://127.0.0.1:7860
    exit /b 0
)

:: Check virtual environment
set "VENV_PY=%FOUND_DIR%\.venv\Scripts\python.exe"
if not exist "%VENV_PY%" (
    echo [ERROR] Virtual environment not found at: %VENV_PY%
    echo Please run setup.ps1 to configure dependencies.
    pause
    exit /b 1
)

echo ==============================================================================
echo                          HYPOCRITICAL SAINT
echo                  Digital Image Steganography Studio
echo            "Innocent on the Outside. Secret on the Inside."
echo ==============================================================================
echo [*] Location: %FOUND_DIR%
echo [*] Starting studio at http://127.0.0.1:7860 ...
echo [*] Opening browser automatically...
echo ==============================================================================

start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:7860"
cd /d "%FOUND_DIR%"
"%VENV_PY%" app.py
exit /b 0
