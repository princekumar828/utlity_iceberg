@echo off
REM Quick Setup for Windows - Lakehouse Explorer Connection Configuration
setlocal enabledelayedexpansion

echo 🚀 Quick Setup for Existing Lakehouse Connection (Windows)
echo ====================================================

REM Check if virtual environment exists
if not exist venv (
    echo ❌ Virtual environment not found. Running setup first...
    call setup.bat
    if errorlevel 1 (
        echo ❌ Setup failed. Please fix the issues and try again.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 📝 Configuration Options:
echo 1. Environment Variables (Recommended)
echo 2. Configuration File
echo.

set /p choice="Choose option (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo 📋 Setting up environment variables...
    echo Please provide your existing lakehouse connection details:
    echo.
    
    set /p NESSIE_URI="Nessie URI (e.g., http://your-nessie:19120/api/v1): "
    set /p S3_ENDPOINT="S3/MinIO Endpoint (e.g., http://your-minio:9000): "
    set /p S3_ACCESS_KEY="S3 Access Key: "
    set /p S3_SECRET_KEY="S3 Secret Key: "
    set /p WAREHOUSE_PATH="Warehouse Path (e.g., s3://your-bucket/): "
    
    REM Create .env file
    echo # Lakehouse Connection Configuration > .env
    echo NESSIE_URI=!NESSIE_URI! >> .env
    echo S3_ENDPOINT=!S3_ENDPOINT! >> .env
    echo S3_ACCESS_KEY=!S3_ACCESS_KEY! >> .env
    echo S3_SECRET_KEY=!S3_SECRET_KEY! >> .env
    echo WAREHOUSE_PATH=!WAREHOUSE_PATH! >> .env
    echo. >> .env
    echo # Optional settings >> .env
    echo NESSIE_REF=main >> .env
    echo S3_REGION=us-east-1 >> .env
    echo SSL_VERIFY=false >> .env
    
    echo ✅ Environment configuration saved to .env
    echo.
    echo 🔄 Loading configuration...
    
    REM Set environment variables for testing
    set NESSIE_URI=!NESSIE_URI!
    set S3_ENDPOINT=!S3_ENDPOINT!
    set S3_ACCESS_KEY=!S3_ACCESS_KEY!
    set S3_SECRET_KEY=!S3_SECRET_KEY!
    set WAREHOUSE_PATH=!WAREHOUSE_PATH!
    set NESSIE_REF=main
    set S3_REGION=us-east-1
    set SSL_VERIFY=false
    
) else if "%choice%"=="2" (
    echo.
    echo 📝 Setting up configuration file...
    echo Please provide your existing lakehouse connection details:
    echo.
    
    set /p NESSIE_URI="Nessie URI (e.g., http://your-nessie:19120/api/v1): "
    set /p S3_ENDPOINT="S3/MinIO Endpoint (e.g., http://your-minio:9000): "
    set /p S3_ACCESS_KEY="S3 Access Key: "
    set /p S3_SECRET_KEY="S3 Secret Key: "
    set /p WAREHOUSE_PATH="Warehouse Path (e.g., s3://your-bucket/): "
    
    REM Create config file
    echo { > config.json
    echo   "nessie_uri": "!NESSIE_URI!", >> config.json
    echo   "nessie_ref": "main", >> config.json
    echo   "s3_endpoint": "!S3_ENDPOINT!", >> config.json
    echo   "s3_access_key": "!S3_ACCESS_KEY!", >> config.json
    echo   "s3_secret_key": "!S3_SECRET_KEY!", >> config.json
    echo   "s3_region": "us-east-1", >> config.json
    echo   "warehouse_path": "!WAREHOUSE_PATH!", >> config.json
    echo   "ssl_verify": false >> config.json
    echo } >> config.json
    
    echo ✅ Configuration saved to config.json
    
) else (
    echo ❌ Invalid choice. Please run the script again.
    pause
    exit /b 1
)

echo.
echo 🧪 Testing connection...

if "%choice%"=="1" (
    python -c "from config import LakehouseConfig; from lakehouse_explorer import LakehouseExplorer; import os; config = LakehouseConfig.from_env(); print('✅ Configuration loaded successfully'); print(f'   Nessie: {config.nessie_uri}'); print(f'   S3: {config.s3_endpoint}'); print(f'   Warehouse: {config.warehouse_path}'); explorer = LakehouseExplorer(config); print('✅ Connected to lakehouse successfully!'); namespaces = explorer.list_namespaces(); print(f'✅ Found {len(namespaces)} namespace(s)')"
) else (
    python -c "from config import LakehouseConfig; from lakehouse_explorer import LakehouseExplorer; config = LakehouseConfig.from_file('config.json'); print('✅ Configuration loaded successfully'); print(f'   Nessie: {config.nessie_uri}'); print(f'   S3: {config.s3_endpoint}'); print(f'   Warehouse: {config.warehouse_path}'); explorer = LakehouseExplorer(config); print('✅ Connected to lakehouse successfully!'); namespaces = explorer.list_namespaces(); print(f'✅ Found {len(namespaces)} namespace(s)')"
)

if errorlevel 1 (
    echo ❌ Connection test failed. Please check your connection details and ensure your lakehouse is running.
) else (
    echo.
    echo 🎉 Setup complete! You can now:
    echo.
    if "%choice%"=="1" (
        echo 🌐 Start Web Interface:
        echo    start_web.bat
        echo.
        echo 🖥️  Use CLI:
        echo    python main.py overview
        echo    python main.py interactive
    ) else (
        echo 🌐 Start Web Interface:
        echo    start_web.bat
        echo.
        echo 🖥️  Use CLI:
        echo    python main.py --config config.json overview
        echo    python main.py --config config.json interactive
    )
    echo.
    echo 📖 For more options, see README.md
)

pause
