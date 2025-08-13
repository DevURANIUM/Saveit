from telethon import TelegramClient, events
import asyncio
import os
import time
from datetime import datetime as dt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API info to get from my.telegram.org
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
handler = os.getenv('HANDLER')

client = TelegramClient('save', api_id, api_hash)
your_user_id = None

@client.on(events.NewMessage(pattern=rf'\{handler}'))
async def download(event):
    global your_user_id

    if your_user_id is None:
        me = await client.get_me()
        your_user_id = me.id

    if event.sender_id != your_user_id:
        return

    pvpv = event.sender_id
    saved_messages_chat_id = "me"
    inpv = await event.client.send_message(pvpv, "Downloading...")

    if event.reply_to_msg_id:
        ok = await event.get_reply_message()
        sssender = ok.sender_id
    else:
        return await event.reply("Reply to a message with media to save it.", time=8)

    await event.delete()

    if not (ok and ok.media):
        await inpv.edit("No media found in the replied message.")
        return

    download_path = "downloads/"
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    try:
        if hasattr(ok.media, "document") or hasattr(ok.media, "photo"):
            file_path = await event.client.download_media(ok, file=download_path)
        else:
            await inpv.edit("Unsupported media type.")
            return
    except Exception as err:
        await inpv.edit(f"Failed to download file: {str(err)}")
        return

    try:
        await event.client.send_file(
            saved_messages_chat_id, 
            file_path, 
            caption=f"File saved from {sssender}",
            force_document=True
        )
    except Exception as err:
        await inpv.edit(f"Failed to send file to Saved Messages: {str(err)}")
        return

    await inpv.delete()

async def main():
    async with client:
        global your_user_id
        me = await client.get_me()
        your_user_id = me.id
        print(f"Bot is running as user: {me.username} (ID: {your_user_id})")
        await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
