import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient, events


load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
handler = os.getenv("HANDLER", ".saveit")
auto_save_timed = os.getenv("AUTO_SAVE_TIMED", "true").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

client = TelegramClient("save", api_id, api_hash)
downloads_path = Path("downloads")
saved_message_ids = set()
save_lock = asyncio.Lock()
your_user_id = None


def is_timed_media(message):
    """Telegram exposes the self-destruct timer on the media object."""
    return bool(
        message
        and message.media
        and getattr(message.media, "ttl_seconds", None)
    )


async def save_media(message, sender_id):
    message_key = (message.chat_id, message.id)

    async with save_lock:
        if message_key in saved_message_ids:
            return
        saved_message_ids.add(message_key)

    downloads_path.mkdir(parents=True, exist_ok=True)

    try:
        file_path = await client.download_media(message, file=str(downloads_path))
        if not file_path:
            raise RuntimeError("Telegram did not return a downloadable file")

        await client.send_file(
            "me",
            file_path,
            caption=f"File saved from {sender_id}",
            force_document=True,
        )
        print(f"Saved media from {sender_id}: {file_path}")
    except Exception:
        async with save_lock:
            saved_message_ids.discard(message_key)
        raise


@client.on(events.NewMessage(incoming=True))
async def auto_save_timed_media(event):
    if not auto_save_timed or not is_timed_media(event.message):
        return

    try:
        await save_media(event.message, event.sender_id)
    except Exception as err:
        print(f"Failed to auto-save timed media {event.chat_id}/{event.id}: {err}")


@client.on(events.NewMessage(pattern=rf"^{handler}$"))
async def download_with_handler(event):
    if event.sender_id != your_user_id:
        return

    status = await event.client.send_message(event.chat_id, "Downloading...")

    if not event.reply_to_msg_id:
        await status.edit("Reply to a message with media to save it.")
        return

    message = await event.get_reply_message()
    await event.delete()

    if not message or not message.media:
        await status.edit("No media found in the replied message.")
        return

    try:
        await save_media(message, str(message.sender_id))
    except Exception as err:
        await status.edit(f"Failed to save media: {err}")
        return

    await status.delete()


async def main():
    global your_user_id

    async with client:
        me = await client.get_me()
        your_user_id = me.id
        print(f"Running as {me.username or me.first_name} (ID: {your_user_id})")
        print(f"Automatic timed-media saving: {'enabled' if auto_save_timed else 'disabled'}")
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
