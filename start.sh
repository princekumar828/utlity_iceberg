#!/bin/bash

# Lakehouse Explorer Web Application Startup Script

echo "🌐 Starting Lakehouse Explorer Web Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for configuration
if [ ! -f "config.json" ] && [ ! -f ".env" ]; then
    echo "⚠️  No configuration found!"
    echo "Please create either:"
    echo "1. config.json file with your lakehouse settings"
    echo "2. .env file with environment variables"
    echo ""
    echo "See config/sample.json for an example."
    exit 1
fi

# Start the web application
echo "🚀 Starting web server..."
echo "📍 Open your browser to: http://localhost:5000"
python app.py
