#!/bin/bash
# Quick start script for macOS/Linux

echo "========================================"
echo "AI Market Analyst Agent - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your Gemini API key!"
    echo "   Open .env and replace 'your_gemini_api_key_here' with your actual key"
    echo ""
    read -p "Press enter to continue after adding your API key..."
fi

# Run installation test
echo "Running installation test..."
python test_installation.py
echo ""

echo "========================================"
echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. Backend: uvicorn src.main:app --reload"
echo "2. Frontend: streamlit run app.py"
echo ""
echo "Or use Docker: docker-compose up --build"
echo "========================================"
