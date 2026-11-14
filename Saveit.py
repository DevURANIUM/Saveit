import asyncio
import csv
import os
from datetime import datetime
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

# catch_up=True: after a disconnect (e.g. Mac sleep), fetch messages that
# arrived meanwhile instead of silently skipping them.
client = TelegramClient("save", api_id, api_hash, catch_up=True)
downloads_path = Path("downloads")
log_path = Path("saves_log.csv")
LOG_FIELDS = [
    "saved_at",
    "status",
    "how",
    "timer_seconds",
    "sender_id",
    "sender_name",
    "chat_id",
    "message_id",
    "file",
    "error",
]
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


def init_log():
    """Create the log; on first run, list files saved before logging existed."""
    if log_path.exists():
        return
    with log_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writeheader()
        if downloads_path.is_dir():
            for p in sorted(downloads_path.iterdir(), key=lambda p: p.stat().st_mtime):
                if p.is_file() and not p.name.startswith("."):
                    saved_at = datetime.fromtimestamp(p.stat().st_mtime)
                    writer.writerow({
                        "saved_at": saved_at.isoformat(timespec="seconds"),
                        "status": "saved",
                        "how": "before log",
                        "file": str(p),
                    })


def write_log(**row):
    row.setdefault("saved_at", datetime.now().isoformat(timespec="seconds"))
    try:
        with log_path.open("a", newline="") as f:
            csv.DictWriter(f, fieldnames=LOG_FIELDS).writerow(row)
    except OSError as err:
        print(f"Could not write to {log_path}: {err}")


async def sender_name(message):
    try:
        sender = await message.get_sender()
    except Exception:
        return ""
    if sender is None:
        return ""
    name = " ".join(
        part for part in (getattr(sender, "first_name", None), getattr(sender, "last_name", None)) if part
    ) or getattr(sender, "title", "") or ""
    username = getattr(sender, "username", None)
    return f"{name} (@{username})" if username else name


async def save_media(message, sender_id, how):
    message_key = (message.chat_id, message.id)

    async with save_lock:
        if message_key in saved_message_ids:
            return
        saved_message_ids.add(message_key)

    downloads_path.mkdir(parents=True, exist_ok=True)
    log_row = {
        "how": how,
        "timer_seconds": getattr(message.media, "ttl_seconds", None) or "",
        "sender_id": sender_id,
        "sender_name": await sender_name(message),
        "chat_id": message.chat_id,
        "message_id": message.id,
    }

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
        write_log(status="saved", file=file_path, **log_row)
    except Exception as err:
        async with save_lock:
            saved_message_ids.discard(message_key)
        write_log(status="failed", error=str(err), **log_row)
        raise


@client.on(events.NewMessage(incoming=True))
async def auto_save_timed_media(event):
    if event.message.media:
        ttl = getattr(event.message.media, "ttl_seconds", None)
        print(
            f"Incoming media {event.chat_id}/{event.id}: "
            f"{type(event.message.media).__name__}, timer={ttl}"
        )

    if not auto_save_timed or not is_timed_media(event.message):
        return

    try:
        await save_media(event.message, event.sender_id, how="auto (timed)")
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
        await save_media(message, str(message.sender_id), how=f"manual ({handler})")
    except Exception as err:
        await status.edit(f"Failed to save media: {err}")
        return

    await status.delete()


async def main():
    global your_user_id

    init_log()
    print(f"Logging saves to {log_path.resolve()}")

    async with client:
        me = await client.get_me()
        your_user_id = me.id
        print(f"Running as {me.username or me.first_name} (ID: {your_user_id})")
        print(f"Automatic timed-media saving: {'enabled' if auto_save_timed else 'disabled'}")
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
