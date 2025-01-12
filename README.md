
# Timed Photo Saver for Telegram (Saveit)

This script automatically saves timed (self-destructing) photos and other media from Telegram chats before they disappear. It uses the [Telethon](https://docs.telethon.dev/) library to interact with the Telegram API and download media files, saving them locally and optionally forwarding them to your Saved Messages in Telegram.

## Features

- Downloads timed/self-destructing media from Telegram chats.
- Saves downloaded media to the `downloads/` folder.
- Forwards downloaded media to your Saved Messages.
- Supports both documents and regular media.

## Requirements

Before running the script, make sure you have:

- **Python 3.9+**
- Python package `telethon`

### Install required Python packages

To install the necessary package, run:

```bash
pip install telethon
```

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/DevURANIUM/Saveit.git
   cd Saveit
   ```

2. **Run the `run.sh` script**:

   This will automate the setup process:

   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   The script will:
   - Create `.env` file if not exists.
   - Ask for your Telegram API credentials.
   - Pull the latest updates from Git.
   - Install or update `telethon`.
   - Run the script.

3. **Manually configure API credentials (optional)**:

   If you prefer to configure manually, open the `.env` file and add:

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

   - Reply to any media in Telegram with `.saveit` (or your chosen handler).
   - The media will be saved to the `downloads/` folder and forwarded to your Saved Messages.

### Example

1. Run the script:

   ```bash
   python3 Saveit.py
   ```

2. In a Telegram chat, reply to a media message with `.saveit` to save it locally and forward it.

## Code Overview

- **Client Setup**: Initializes the Telegram client using the provided API credentials.
- **Command Listener**: Listens for `.saveit` commands in chats.
- **Media Handling**: Downloads and forwards media.

## Dependencies

- [Telethon](https://github.com/LonamiWebs/Telethon) - A Python library for interacting with the Telegram API.

## License

This project is licensed under the MIT License.

## Support & Contributions

For any issues or suggestions, contact:

- [Telegram](https://t.me/DevURANIUM)
- [GitHub Issues](https://github.com/DevURANIUM/Saveit/issues)

## Donation Links

Support the project:

- **BTC**: `bc1qcclcp574hnznm0nmdzzf0ta7366svjskttqks3`
- **TRON**: `TXJqhhwvkrTdnf5HReZf55hEzZuxjto3R4`
- **USDT-(TRC20)**: `TXJqhhwvkrTdnf5HReZf55hEzZuxjto3R4`
- **TON**: `UQAJH2N0pqpvC9YN841w5NH1dCN9Lakwkpjvoy7vXf-vfqgv`
