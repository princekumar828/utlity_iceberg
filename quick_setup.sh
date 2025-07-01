#!/bin/bash

# Quick Setup Guide for Existing Lakehouse
echo "🚀 Quick Setup for Existing Lakehouse Connection"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Running setup first..."
    ./setup.sh
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📝 Configuration Options:"
echo "1. Environment Variables (Recommended)"
echo "2. Configuration File"
echo ""

read -p "Choose option (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "📋 Setting up environment variables..."
    echo "Please provide your existing lakehouse connection details:"
    echo ""
    
    read -p "Nessie URI (e.g., http://your-nessie:19120/api/v1): " NESSIE_URI
    read -p "S3/MinIO Endpoint (e.g., http://your-minio:9000): " S3_ENDPOINT
    read -p "S3 Access Key: " S3_ACCESS_KEY
    read -s -p "S3 Secret Key: " S3_SECRET_KEY
    echo ""
    read -p "Warehouse Path (e.g., s3://your-bucket/): " WAREHOUSE_PATH
    
    # Create .env file
    cat > .env << EOF
# Lakehouse Connection Configuration
NESSIE_URI=$NESSIE_URI
S3_ENDPOINT=$S3_ENDPOINT
S3_ACCESS_KEY=$S3_ACCESS_KEY
S3_SECRET_KEY=$S3_SECRET_KEY
WAREHOUSE_PATH=$WAREHOUSE_PATH

# Optional settings
NESSIE_REF=main
S3_REGION=us-east-1
SSL_VERIFY=false
EOF
    
    echo "✅ Environment configuration saved to .env"
    echo ""
    echo "🔄 Loading configuration..."
    source .env
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "📝 Setting up configuration file..."
    echo "Please provide your existing lakehouse connection details:"
    echo ""
    
    read -p "Nessie URI (e.g., http://your-nessie:19120/api/v1): " NESSIE_URI
    read -p "S3/MinIO Endpoint (e.g., http://your-minio:9000): " S3_ENDPOINT
    read -p "S3 Access Key: " S3_ACCESS_KEY
    read -s -p "S3 Secret Key: " S3_SECRET_KEY
    echo ""
    read -p "Warehouse Path (e.g., s3://your-bucket/): " WAREHOUSE_PATH
    
    # Create config file
    cat > config.json << EOF
{
  "nessie_uri": "$NESSIE_URI",
  "nessie_ref": "main",
  "s3_endpoint": "$S3_ENDPOINT",
  "s3_access_key": "$S3_ACCESS_KEY",
  "s3_secret_key": "$S3_SECRET_KEY",
  "s3_region": "us-east-1",
  "warehouse_path": "$WAREHOUSE_PATH",
  "ssl_verify": false
}
EOF
    
    echo "✅ Configuration saved to config.json"
    export LAKEHOUSE_CONFIG_FILE="config.json"
    
else
    echo "❌ Invalid choice. Please run the script again."
    exit 1
fi

echo ""
echo "🧪 Testing connection..."

if [ "$choice" = "1" ]; then
    python -c "
from config import LakehouseConfig
from lakehouse_explorer import LakehouseExplorer
import os

try:
    config = LakehouseConfig.from_env()
    print('✅ Configuration loaded successfully')
    print(f'   Nessie: {config.nessie_uri}')
    print(f'   S3: {config.s3_endpoint}')
    print(f'   Warehouse: {config.warehouse_path}')
    
    explorer = LakehouseExplorer(config)
    print('✅ Connected to lakehouse successfully!')
    
    namespaces = explorer.list_namespaces()
    print(f'✅ Found {len(namespaces)} namespace(s)')
    
except Exception as e:
    print(f'❌ Connection test failed: {e}')
    print('   Please check your connection details and ensure your lakehouse is running.')
"
else
    python -c "
from config import LakehouseConfig
from lakehouse_explorer import LakehouseExplorer

try:
    config = LakehouseConfig.from_file('config.json')
    print('✅ Configuration loaded successfully')
    print(f'   Nessie: {config.nessie_uri}')
    print(f'   S3: {config.s3_endpoint}')
    print(f'   Warehouse: {config.warehouse_path}')
    
    explorer = LakehouseExplorer(config)
    print('✅ Connected to lakehouse successfully!')
    
    namespaces = explorer.list_namespaces()
    print(f'✅ Found {len(namespaces)} namespace(s)')
    
except Exception as e:
    print(f'❌ Connection test failed: {e}')
    print('   Please check your connection details and ensure your lakehouse is running.')
"
fi

echo ""
echo "🎉 Setup complete! You can now:"
echo ""
if [ "$choice" = "1" ]; then
    echo "🌐 Start Web Interface:"
    echo "   source .env && ./start_web.sh"
    echo ""
    echo "🖥️  Use CLI:"
    echo "   source .env && python main.py overview"
    echo "   source .env && python main.py interactive"
else
    echo "🌐 Start Web Interface:"
    echo "   ./start_web.sh"
    echo ""
    echo "🖥️  Use CLI:"
    echo "   python main.py --config config.json overview"
    echo "   python main.py --config config.json interactive"
fi
echo ""
echo "📖 For more options, see README.md"
