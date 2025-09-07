@echo off
echo 🎓 Campus Event Reporting System - Web Interface Launcher
echo ============================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found. Please run this from the project directory.
    pause
    exit /b 1
)

REM Check if HTML file exists
if not exist "sql_query_interface.html" (
    echo ❌ sql_query_interface.html not found.
    pause
    exit /b 1
)

echo ✅ Starting web interface...
echo.

REM Start the Python launcher
python launch_web_interface.py

pause
