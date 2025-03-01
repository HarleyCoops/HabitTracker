@echo off
echo Productivity and Mood Tracker
echo ============================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if the virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies if needed
if not exist venv\Lib\site-packages\google (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the main script
python src\main.py %*

REM Deactivate the virtual environment
call venv\Scripts\deactivate

pause 