from telethon import TelegramClient, events
import asyncio
import os
import subprocess
import time
from datetime import datetime as dt

# API info to get from my.telegram.org
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

client = TelegramClient('save', api_id, api_hash)

def check_and_install(package, install_command):
    try:
        subprocess.run([package, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{package} is already installed.")
    except subprocess.CalledProcessError:
        print(f"{package} is not installed. Installing now...")
        os.system(install_command)

check_and_install('mediainfo', 'apt install mediainfo -y')
check_and_install('ffmpeg', 'apt install ffmpeg -y')

@client.on(events.NewMessage(pattern=r'\.saveit'))
async def download(event):
    pvpv = event.sender_id
    saved_messages_chat_id = "me"
    inpv = await event.client.send_message(pvpv, "Downloading...")

    if event.reply_to_msg_id:
        ok = await event.get_reply_message()
        sssender = ok.sender_id
        sschat = event.chat_id
    else:
        return await event.reply("Reply to a message with media to save it.", time=8)
    
    await event.delete()

    if not (ok and ok.media):
        return

    s = dt.now()
    k = time.time()

    download_path = "downloads/"
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    if hasattr(ok.media, "document"):
        file = ok.media.document
        mime_type = file.mime_type
        filename = ok.file.name if ok.file.name else "file_unknown"

        try:
            result = await event.client.download_media(ok, file=f"{download_path}{filename}")
        except Exception as err:
            await inpv.edit(f"Failed to download file: {str(err)}")
            return

        file_name = result
    else:
        file_name = await event.client.download_media(ok, download_path)

    e = dt.now()
    t = int((e - s).seconds * 1000)

    if os.path.exists(file_name):
        await event.client.send_file(saved_messages_chat_id, file_name, caption=f"File saved by {sssender} ")
    else:
        await event.client.send_message(pvpv, "File not found after download.")

    await inpv.delete()

async def main():
    async with client:
        await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
