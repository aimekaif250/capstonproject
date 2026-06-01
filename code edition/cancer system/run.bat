@echo off
cd /d "%~dp0"

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3.11 -V >nul 2>nul && set PYTHON=py -3.11 || set PYTHON=python
) else (
  set PYTHON=python
)

if not exist "venv\Scripts\python.exe" (
  %PYTHON% -m venv venv
  venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
  venv\Scripts\python.exe -m pip install -r requirements.txt
)

rem Start Flask in a new window so we can open browser immediately
start "" cmd /k "venv\Scripts\python.exe app.py"

rem Wait a few seconds then open browser
timeout /t 3 /nobreak >nul
start "" "http://localhost:5000"

pause
