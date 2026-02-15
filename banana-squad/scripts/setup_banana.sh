#!/bin/bash
# Banana Squad - Dependency Setup
# Run once to install required Python packages for image generation.

set -e

echo "Installing Banana Squad dependencies..."
pip install google-genai Pillow python-dotenv
echo ""
echo "Banana Squad dependencies installed successfully."
echo ""
echo "Next steps:"
echo "  1. Set your Gemini API key: export GEMINI_API_KEY='your-key-here'"
echo "     Or add GEMINI_API_KEY=your-key-here to a .env file"
echo "  2. Run: /banana-squad:banana-squad to start generating images"
