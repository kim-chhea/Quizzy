#!/bin/bash
# Quick start script for Quizzy with Multiplayer

echo "🎮 Starting Quizzy - Multiplayer Quiz Game"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Streamlit app..."
echo ""
echo "📱 Features:"
echo "   - Solo Practice Mode"
echo "   - Host Multiplayer Games"
echo "   - Join Games with QR or PIN"
echo "   - Live Leaderboards"
echo ""
echo "Opening browser..."
streamlit run app.py
