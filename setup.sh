#!/bin/bash

# ============================================
# 10X Stock Scanner - First-Time Setup
# ============================================
# Run this once after cloning the repo

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "  10X Stock Scanner - Setup"
echo "=========================================="
echo ""

# Setup Python backend
echo "Setting up Python backend..."
cd "$SCRIPT_DIR/backend"
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
echo "Backend dependencies installed."
echo ""

# Setup React frontend
echo "Setting up React frontend..."
cd "$SCRIPT_DIR/frontend"
npm install --silent
echo "Frontend dependencies installed."
echo ""

echo "=========================================="
echo "  Setup complete!"
echo "=========================================="
echo ""
echo "Run: ./start.sh"
