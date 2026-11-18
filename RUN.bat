@echo off
setlocal enabledelayedexpansion

title HYPOCRITICAL SAINT - Digital Image Steganography Studio
cd /d "%~dp0"

echo ==============================================================================
echo                          HYPOCRITICAL SAINT
echo                  Digital Image Steganography Studio
echo            "Innocent on the Outside. Secret on the Inside."
echo ==============================================================================
echo  Course:     Digital Image Processing
echo  Developer:  Um Al-Baneen Awwad (أم البنين عواد)
echo  College:    College of Engineering, University of Basrah (2026-2027)
echo ==============================================================================
echo.

:: 1. Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo [!] Virtual environment (.venv) not found.
    echo [*] Creating virtual environment with Python 3.12...
    
    where py >nul 2>&1
    if !errorlevel! equ 0 (
        py -3.12 -m venv .venv
    ) else (
        python -m venv .venv
    )
    
    if not exist ".venv\Scripts\activate.bat" (
        echo [ERROR] Failed to create virtual environment!
        echo Please ensure Python 3.12 is installed and available.
        pause
        exit /b 1
    )
    
    echo [*] Installing required dependencies...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -e . gradio
) else (
    call .venv\Scripts\activate.bat
)

:: 2. Verify dependencies
echo [*] Verifying environment and dependencies...
python -c "import stegano, gradio, PIL, cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Missing dependencies detected. Installing...
    pip install -e . gradio
)

echo [OK] Dependencies verified successfully.
echo.
echo ==============================================================================
echo [*] Launching HYPOCRITICAL SAINT Studio at http://127.0.0.1:7860
echo [*] Opening default web browser automatically...
echo [*] Press Ctrl+C in this terminal window to stop the server.
echo ==============================================================================
echo.

:: 3. Launch browser in background after short delay
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:7860"

:: 4. Run application
python app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application exited with error code %errorlevel%.
    pause
)
