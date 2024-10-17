from telethon import TelegramClient, events
import asyncio
import os
import subprocess
import time
from datetime import datetime as dt

# اطلاعات API که باید از my.telegram.org بگیرید
api_id = '15158919'
api_hash = '8fd34311e66d16b2a79566353349ad28'

# ساخت یک کلاینت تلگرام
client = TelegramClient('save', api_id, api_hash)

# تابع برای چک کردن و نصب بسته‌های مورد نیاز
def check_and_install(package, install_command):
    try:
        # بررسی می‌کنیم که آیا بسته نصب است یا خیر
        subprocess.run([package, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{package} is already installed.")
    except subprocess.CalledProcessError:
        # اگر نصب نبود، دستور نصب را اجرا می‌کنیم
        print(f"{package} is not installed. Installing now...")
        os.system(install_command)

# چک کردن و نصب mediainfo
check_and_install('mediainfo', 'apt install mediainfo -y')

# چک کردن و نصب ffmpeg
check_and_install('ffmpeg', 'apt install ffmpeg -y')

@client.on(events.NewMessage(pattern=r'\.saveit'))
async def download(event):
    pvpv = event.sender_id
    saved_messages_chat_id = "me"  # شناسه‌ی پیام‌های ذخیره‌شده (Saved Messages)
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

    # ذخیره‌سازی فایل در پوشه‌ی downloads
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

    # چک کردن وجود فایل قبل از ارسال
    if os.path.exists(file_name):
        # ارسال فایل به پیام‌های ذخیره‌شده (Saved Messages)
        await event.client.send_file(saved_messages_chat_id, file_name, caption=f"File saved by {sssender} ")
    else:
        await event.client.send_message(pvpv, "File not found after download.")

    # حذف پیام‌های موقت
    await inpv.delete()

async def main():
    # شروع کلاینت و وارد شدن به حساب تلگرام
    async with client:
        await client.run_until_disconnected()

# اجرای برنامه
if __name__ == "__main__":
    asyncio.run(main())
