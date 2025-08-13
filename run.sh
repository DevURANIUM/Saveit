#!/bin/bash
set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR"

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it first."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install it first."
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "Creating .env file based on .env.example..."
    cp .env.example .env

    echo "Please enter your Telegram API credentials:"
    read -p "API_ID: " api_id
    read -p "API_HASH: " api_hash
    read -p "HANDLER (e.g., .saveit): " handler

    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/API_ID=.*/API_ID=$api_id/" .env
        sed -i '' "s/API_HASH=.*/API_HASH=$api_hash/" .env
        sed -i '' "s/HANDLER=.*/HANDLER=$handler/" .env
    else
        sed -i "s/API_ID=.*/API_ID=$api_id/" .env
        sed -i "s/API_HASH=.*/API_HASH=$api_hash/" .env
        sed -i "s/HANDLER=.*/HANDLER=$handler/" .env
    fi
fi

git stash || true
git pull || true
git stash pop || true

if pip show telethon &> /dev/null; then
    echo "Telethon is already installed. Checking for updates..."
    pip install --upgrade telethon
else
    echo "Telethon is not installed. Installing now..."
    pip install telethon
fi

echo "Running Saveit.py..."
python3 Saveit.py

echo "Done."
