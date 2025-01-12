#!/bin/bash

if [ ! -f ".env" ]; then
    echo "Creating .env file based on .env-example..."
    cp .env-example .env

    echo "Please enter your Telegram API credentials:"
    read -p "API_ID: " api_id
    read -p "API_HASH: " api_hash
    read -p "HANDLER (e.g., .saveit): " handler

    sed -i "s/API_ID=.*/API_ID=$api_id/" .env
    sed -i "s/API_HASH=.*/API_HASH=$api_hash/" .env
    sed -i "s/HANDLER=.*/HANDLER=$handler/" .env
fi

git stash
git pull
git stash pop

if pip show telethon &> /dev/null; then
    echo "Telethon is already installed. Checking for updates..."
    pip install --upgrade telethon
else
    echo "Telethon is not installed. Installing now..."
    pip install telethon
fi

# Run the Saveit.py script
python3 Saveit.py

echo "done."

