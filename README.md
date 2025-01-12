
# Timed Photo Saver for Telegram (Saveit)

This script automatically saves timed (self-destructing) photos and other media from Telegram chats before they disappear. It uses the [Telethon](https://docs.telethon.dev/) library to interact with the Telegram API and download media files, saving them locally and optionally forwarding them to your Saved Messages in Telegram.

## Features

- Downloads timed/self-destructing media in Telegram chats.
- Saves downloaded media to the `downloads/` folder.
- Automatically forwards the downloaded files to the user's Saved Messages.
- Handles both document-based media and regular media.

## Requirements

Before running the script, ensure you have the following installed:

- **Python 3.9+**
- Required Python packages:
  - `telethon` (for interacting with Telegram API)

### Installing the required Python packages

You can install the necessary Python packages by running:

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
   Instead of manually setting up the environment and installing dependencies, you can use the `run.sh` script to automate the process.

   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   The script will:
   - Automatically create the `.env` file if it doesn't exist.
   - Prompt you to enter your Telegram API credentials (`API_ID`, `API_HASH`) and the command handler (e.g., `.saveit`).
   - Pull the latest changes from the Git repository.
   - Install or update the required `telethon` package.
   - Run the `Saveit.py` script.

3. **Configure API credentials**:
   If you prefer to configure the API credentials manually, you can open the `.env` file and set the following:
   
   ```
   API_ID=YOUR_API_ID
   API_HASH=YOUR_API_HASH
   HANDLER=.saveit  # Change this to any command prefix you prefer, e.g., .s or !save
   ```

## How to Use

1. **Run the script**:
   You can start the script by running:
   ```bash
   python3 Saveit.py
   ```

2. **Trigger media download**:
   - To download a photo or document, reply to a message containing the media in any chat and send `.saveit` (or your chosen handler).
   - The media will be saved to the `downloads/` folder on your local system and automatically forwarded to your Saved Messages in Telegram.

### Example

1. Run the script:

   ```bash
   python3 Saveit.py
   ```

2. In a Telegram chat, reply to a media message with `.saveit` (or your chosen handler) to save it locally and forward it to your Saved Messages.

## Code Overview

- **Client Setup**: Initializes the Telegram client using the provided API credentials.
- **Command Listener**: Listens for `.saveit` commands in Telegram chats, triggered by replying to messages.
- **Media Handling**: Downloads media files to the local system (`downloads/` folder) and forwards them to the Saved Messages chat.

## Dependencies

- [Telethon](https://github.com/LonamiWebs/Telethon) - Python library to interact with Telegram's API.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support & Contributions

If you encounter any issues or have suggestions for improvement, please reach out via:

- [Telegram](https://t.me/DevURANIUM)
- [GitHub Issues](https://github.com/DevURANIUM/Saveit/issues)

## Donation Links

Support the project through donations:

- **BTC**: `bc1qcclcp574hnznm0nmdzzf0ta7366svjskttqks3`
- **TRON**: `TXJqhhwvkrTdnf5HReZf55hEzZuxjto3R4`
- **USDT-(TRC20)**: `TXJqhhwvkrTdnf5HReZf55hEzZuxjto3R4`
- **TON**: `UQAJH2N0pqpvC9YN841w5NH1dCN9Lakwkpjvoy7vXf-vfqgv`
```
