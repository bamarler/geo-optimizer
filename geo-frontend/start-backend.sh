#!/bin/bash

cd "$(dirname "$0")/server"

# Activate virtual environment
source venv/bin/activate

# Start Flask server
echo "🚀 Starting GEO Backend Server..."
echo "📍 Server running on http://localhost:5001"
echo ""
python app.py

