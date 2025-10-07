#!/bin/bash

# AI Copilot Backend Startup Script

echo "🚀 Starting AI Copilot Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -e .
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GOOGLE_GEMINI_API_KEY"
    echo "Press Enter to continue with mock mode, or Ctrl+C to exit and configure..."
    read
fi

# Start the server
echo "✅ Starting server on http://localhost:3001"
echo "📚 API Documentation: http://localhost:3001/docs"
echo ""

python -m uvicorn app.main:app --host 0.0.0.0 --port 3001 --reload
