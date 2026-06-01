@echo off
echo ========================================
echo Cancer Risk Prediction System Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not found in PATH!
    echo.
    echo This can happen if you installed Python from Microsoft Store.
    echo.
    echo SOLUTION 1: Add Python to PATH
    echo 1. Search for "Environment Variables" in Windows search
    echo 2. Click "Environment Variables"
    echo 3. Under "System variables", find "Path" and click "Edit"
    echo 4. Add this path: C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\
    echo 5. Restart Command Prompt and try again
    echo.
    echo SOLUTION 2: Download Python from python.org
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.8 or higher
    echo 3. Install and check "Add Python to PATH"
    echo 4. Run this script again
    echo.
    echo SOLUTION 3: Use PowerShell setup
    echo Run: .\setup.ps1
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python found!
)

echo.
echo Step 2: Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo ✅ Virtual environment created.
) else (
    echo ✅ Virtual environment already exists.
)

echo.
echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 4: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 5: Verifying installation...
pip list | findstr "Flask"
if %errorlevel% neq 0 (
    echo ❌ Flask installation failed!
    pause
    exit /b 1
) else (
    echo ✅ Flask installed successfully.
)

echo.
echo ========================================
echo Setup Complete! 🎉
echo ========================================
echo.
echo To run the application:
echo 1. Run: run.bat
echo 2. Open: http://localhost:5000
echo.
echo Your cancer risk prediction system is ready!
echo.
pause