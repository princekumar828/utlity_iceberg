#!/bin/bash

# Lakehouse Explorer Setup Script
# This script helps set up the environment for the lakehouse explorer tool

echo "🚀 Setting up Lakehouse Explorer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Make main.py executable
chmod +x main.py

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Create configuration:"
echo "   - Set environment variables (see README.md), OR"
echo "   - Run: python main.py setup --output config.json"
echo "3. Start exploring: python main.py overview"
echo ""
echo "📖 For more information, see README.md"
