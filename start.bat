@echo off
REM Lakehouse Explorer Web Application Startup Script for Windows

echo 🌐 Starting Lakehouse Explorer Web Application...

REM Check if virtual environment exists
if not exist venv (
    echo ❌ Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check for configuration
if not exist config.json if not exist .env (
    echo ⚠️  No configuration found!
    echo Please create either:
    echo 1. config.json file with your lakehouse settings
    echo 2. .env file with environment variables
    echo.
    echo See config\sample.json for an example.
    pause
    exit /b 1
)

REM Start the web application
echo 🚀 Starting web server...
echo 📍 Open your browser to: http://localhost:5000
python app.py

pause
