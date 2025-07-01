@echo off
REM Lakehouse Explorer Setup Script for Windows
echo 🚀 Setting up Lakehouse Explorer on Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Create virtual environment
echo 🔄 Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, removing old one...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📥 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Test the setup
echo 🧪 Testing setup...
python test_setup.py
if errorlevel 1 (
    echo ❌ Setup test failed
    pause
    exit /b 1
)

echo ✅ Setup complete!
echo.
echo 🎯 Next steps:
echo 1. Configure your lakehouse connection:
echo    - Run: quick_setup.bat
echo    - Or manually edit .env.template and rename to .env
echo.
echo 2. Start exploring:
echo    - Web Interface: start_web.bat
echo    - CLI: python main.py interactive
echo.
echo 📖 For more information, see README.md

pause
