@echo off
REM Start Web Interface for Windows
echo 🌐 Starting Lakehouse Explorer Web Interface...

REM Check if virtual environment exists
if not exist venv (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Load environment variables if .env exists
if exist .env (
    echo 📁 Loading environment variables from .env...
    for /f "usebackq tokens=1,* delims==" %%i in (.env) do (
        if not "%%i"=="" if not "%%i:~0,1%"=="#" (
            set "%%i=%%j"
        )
    )
)

REM Check configuration
echo 🔧 Checking configuration...
if exist config.json (
    echo ✅ Found config.json
    set CONFIG_ARG=--config config.json
) else if defined NESSIE_URI (
    echo ✅ Using environment variables
    set CONFIG_ARG=
) else (
    echo ❌ No configuration found!
    echo Please run quick_setup.bat first to configure your connection.
    pause
    exit /b 1
)

echo.
echo 🚀 Starting web server...
echo Web interface will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start the web application
python web_app.py

pause
