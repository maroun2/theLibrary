#!/bin/bash
set -e

VENV_PATH="$HOME/theLibrary/venv"

echo "Creating virtual environment at $VENV_PATH..."
python3 -m venv "$VENV_PATH"

echo "Installing dependencies..."
"$VENV_PATH/bin/pip" install --upgrade pip
"$VENV_PATH/bin/pip" install requests beautifulsoup4 py7zr

echo ""
echo "Installation complete! Running theLibrary to complete setup..."
echo ""

cd "$(dirname "$0")"
"$VENV_PATH/bin/python3" theLibrary.py
