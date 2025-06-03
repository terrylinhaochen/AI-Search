#!/bin/bash

echo "🚀 Starting AI Book Search..."
echo "Make sure you've set your OpenAI API key in .env file!"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your OpenAI API key"
    exit 1
fi

# Check if requirements are installed
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🌐 Launching Streamlit app..."
echo "The app will open in your browser at http://localhost:8501"
echo ""

streamlit run app.py 