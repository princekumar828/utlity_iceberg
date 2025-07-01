#!/bin/bash

# Web Interface Startup Script
# This script starts the Lakehouse Explorer web interface

echo "🌐 Starting Lakehouse Explorer Web Interface..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if configuration exists
CONFIG_FILE=""
if [ -f "config.json" ]; then
    CONFIG_FILE="config.json"
    echo "✅ Using config.json"
elif [ -f "sample-config.json" ]; then
    CONFIG_FILE="sample-config.json"
    echo "⚠️  Using sample-config.json (update with your values)"
else
    echo "⚠️  No configuration file found. Will try environment variables."
fi

# Set configuration file environment variable
if [ ! -z "$CONFIG_FILE" ]; then
    export LAKEHOUSE_CONFIG_FILE="$CONFIG_FILE"
fi

# Set default port if not specified
if [ -z "$PORT" ]; then
    export PORT=5000
fi

# Start the web application
echo "🚀 Starting web server on port $PORT..."
echo "📱 Open your browser and go to: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run with gunicorn in production mode or Flask dev server
if [ "$FLASK_ENV" = "production" ]; then
    echo "🏭 Running in production mode with gunicorn..."
    gunicorn --bind 0.0.0.0:$PORT --workers 4 web_app:app
else
    echo "🛠️  Running in development mode..."
    export FLASK_DEBUG=true
    python web_app.py
fi
