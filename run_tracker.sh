#!/bin/bash

echo "Productivity and Mood Tracker"
echo "============================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in the PATH."
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -d "venv/lib/python*/site-packages/google" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the main script
python3 src/main.py "$@"

# Deactivate the virtual environment
deactivate 