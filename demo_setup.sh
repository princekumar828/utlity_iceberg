#!/bin/bash

# Demo: How to Use the Lakehouse Explorer Setup
echo "🎬 DEMO: Lakehouse Explorer Setup and Usage"
echo "==========================================="

echo ""
echo "This demo shows you exactly how to set up and use the Lakehouse Explorer."
echo "We'll walk through each step with explanations."
echo ""

# Function to pause and wait for user
pause_demo() {
    echo ""
    read -p "👆 Press Enter to continue to the next step..."
    echo ""
}

# Step 1: Check current directory
echo "📍 Step 1: Verify we're in the right directory"
echo "Current directory: $(pwd)"
echo "Files available:"
ls -la | grep -E "\.(py|sh|md|txt|json)$" | head -10
pause_demo

# Step 2: Show setup process
echo "🛠️  Step 2: Initial Setup"
echo "This creates a virtual environment and installs dependencies:"
echo ""
echo "Command: ./setup.sh"
echo ""
echo "What it does:"
echo "- Creates Python virtual environment"
echo "- Installs all required packages"
echo "- Verifies everything works"
echo ""
echo "Run this now? (y/n)"
read -p "> " run_setup

if [ "$run_setup" = "y" ]; then
    if [ -f "setup.bat" ] && [ "$OS" = "Windows_NT" ]; then
        setup.bat
    else
        ./setup.sh
    fi
else
    echo "⏭️  Skipping setup (assuming already done)"
fi
pause_demo

# Step 3: Show configuration options
echo "⚙️  Step 3: Configuration Options"
echo "You need to connect to YOUR existing lakehouse."
echo ""
echo "You have two options:"
echo "1. Environment Variables (.env file) - Recommended"
echo "2. Configuration File (config.json)"
echo ""
echo "Both methods require the same information:"
echo "- Nessie URI (your catalog endpoint)"
echo "- S3/MinIO endpoint (your storage endpoint)"  
echo "- S3 credentials (access key & secret)"
echo "- Warehouse path (S3 bucket path)"
echo ""
echo "Example values:"
echo "- Nessie URI: http://localhost:19120/api/v1"
echo "- S3 Endpoint: http://localhost:9000"
echo "- S3 Access Key: minioadmin"
echo "- S3 Secret Key: minioadmin"
echo "- Warehouse Path: s3://warehouse/"
pause_demo

# Step 4: Show quick setup process
echo "🚀 Step 4: Interactive Configuration"
echo "The quick_setup.sh script guides you through configuration:"
echo ""
echo "Command: ./quick_setup.sh"
echo ""
echo "What it does:"
echo "1. Asks for your connection details"
echo "2. Creates .env file or config.json"
echo "3. Tests the connection"
echo "4. Shows next steps"
echo ""
echo "Run configuration now? (y/n)"
read -p "> " run_config

if [ "$run_config" = "y" ]; then
    echo "🎯 Starting interactive configuration..."
    ./quick_setup.sh
else
    echo "⏭️  Skipping configuration"
    echo ""
    echo "💡 You can run './quick_setup.sh' anytime to configure your connection"
fi
pause_demo

# Step 5: Show usage options
echo "🎯 Step 5: How to Use the Explorer"
echo ""
echo "Once configured, you have several options:"
echo ""
echo "Option A: Web Interface (Recommended for beginners)"
echo "  Command: ./start_web.sh"
echo "  Result: Opens http://localhost:5000 with modern UI"
echo "  Features: Visual browsing, search, data preview"
echo ""
echo "Option B: Interactive CLI"
echo "  Command: python main.py interactive"
echo "  Result: User-friendly command-line interface"
echo "  Features: Guided exploration, menu-driven"
echo ""
echo "Option C: Direct CLI Commands"
echo "  Command: python main.py overview"
echo "  Result: Show all namespaces and tables"
echo "  Other commands: list-tables, show-table, preview-table"
pause_demo

# Step 6: Demonstrate if configured
echo "🧪 Step 6: Testing (if configured)"

if [ -f ".env" ] || [ -f "config.json" ]; then
    echo "Configuration found! Let's test it:"
    echo ""
    
    # Activate environment
    if [ -d "venv" ]; then
        echo "🔄 Activating virtual environment..."
        source venv/bin/activate
    fi
    
    # Load env if exists
    if [ -f ".env" ]; then
        echo "📁 Loading environment variables..."
        source .env
        echo "✅ Environment loaded"
        
        echo ""
        echo "🧪 Testing connection..."
        python -c "
from config import LakehouseConfig
try:
    config = LakehouseConfig.from_env()
    print('✅ Configuration is valid')
    print(f'   Nessie: {config.nessie_uri}')
    print(f'   S3: {config.s3_endpoint}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
"
    elif [ -f "config.json" ]; then
        echo "📁 Found config.json file"
        echo "✅ Configuration ready"
        
        echo ""
        echo "🧪 Testing connection..."
        python -c "
from config import LakehouseConfig
try:
    config = LakehouseConfig.from_file('config.json')
    print('✅ Configuration is valid')
    print(f'   Nessie: {config.nessie_uri}')
    print(f'   S3: {config.s3_endpoint}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
"
    fi
    
    echo ""
    echo "🎯 Next steps:"
    echo "1. Start web interface: ./start_web.sh"
    echo "2. Try interactive CLI: python main.py interactive"
    echo "3. Get overview: python main.py overview"
    
else
    echo "ℹ️  No configuration found yet."
    echo "Run './quick_setup.sh' to configure your lakehouse connection."
fi

echo ""
echo "🎉 Demo Complete!"
echo "=================="
echo ""
echo "📖 For detailed information:"
echo "- Read GETTING_STARTED.md for comprehensive guide"
echo "- Read QUICK_START.md for quick reference"
echo "- Read README.md for full documentation"
echo ""
echo "🚀 Happy exploring your lakehouse data!"
