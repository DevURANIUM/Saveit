# Timed Photo Saver for Telegram (Saveit)

This script automatically saves timed (self-destructing) photos and other media from Telegram chats before they disappear. It uses the [Telethon](https://docs.telethon.dev/) library to interact with the Telegram API and download media files, saving them locally and **forwarding them to your Saved Messages as original files without compression**.

## Features

* Downloads timed/self-destructing media from Telegram chats.
* Saves downloaded media to the `downloads/` folder.
* Forwards downloaded media to your Saved Messages **as original files** (no compression).
* Supports documents, photos, and videos.

## Requirements

Before running the script, make sure you have:

* **Python 3.9+**
* Python package `telethon`

### Install required Python packages

```bash
pip install telethon
```

## Setup

1. **Clone the repository**:

```bash
git clone https://github.com/DevURANIUM/Saveit.git
cd Saveit
```

2. **Run the `run.sh` script** (Linux/macOS) or `run.bat` (Windows):

```bash
chmod +x run.sh
./run.sh
```

or on Windows:

```bat
run.bat
```

The script will:

* Create a `.env` file if it does not exist.
* Ask for your Telegram API credentials.
* Pull the latest updates from Git.
* Install or update Telethon.
* Run `Saveit.py`.

3. **Manually configure API credentials (optional)**:

Open the `.env` file and add:

```
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
HANDLER=.saveit  # Or change to another prefix
```

## How to Use

1. **Run the script**:

```bash
python3 Saveit.py
```

2. **Save media**:

* Reply to any media in Telegram with `.saveit` (or your chosen handler).
* The media will be saved to the `downloads/` folder and forwarded to your Saved Messages **as original files**.

### Example

1. Run the script:

```bash
python3 Saveit.py
```

2. In a Telegram chat, reply to a media message with `.saveit` to save it locally and forward it without compression.

## Code Overview

* **Client Setup**: Initializes the Telegram client using the provided API credentials.
* **Command Listener**: Listens for `.saveit` commands in chats.
* **Media Handling**: Downloads media and forwards it to Saved Messages **as original files**.

## Dependencies

* [Telethon](https://github.com/LonamiWebs/Telethon) - A Python library for interacting with the Telegram API.

## License

This project is licensed under the MIT License.

## Support & Contributions

For any issues or suggestions, contact:

* [Telegram](https://t.me/DevURANIUM)
* [GitHub Issues](https://github.com/DevURANIUM/Saveit/issues)

## Donation Links

Support the project:

- **BTC**: `bc1qcclcp574hnznm0nmdzzf0ta7366svjskttqks3`
- **LTC**: `ltc1qcrkelw38gjrmg0ptjy2nshqej622kp76het7q0`
- **XRP**: `rPoK5SBChFPqEiQv1W97LW6FKoJZLipDVQ`
- **XLM**: `GDMUQREEZNBSTQOT5BV7MYEMXJFV3CYRZXUVOYCTIUZTHUWPHLVASFVD`
- **TON**: `UQAJH2N0pqpvC9YN841w5NH1dCN9Lakwkpjvoy7vXf-vfqgv`
- **TRON**: `TXJqhhwvkrTdnf5HReZf55hEzZuxjto3R4`
- **USDT(BEP20)**: `0x1591036c4bD05b046532B65Df939fcd7824E18c7`
