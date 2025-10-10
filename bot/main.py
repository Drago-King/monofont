import logging
from pyrogram import Client, filters
from config.settings import API_ID, API_HASH, BOT_TOKEN
from .handlers import handle_single_file, handle_album

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = Client(
    "monospace_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "👋 **Welcome!**\n\nSend me any file or media with a caption, and I'll resend it with the caption formatted in **monospace** text."
    )

@app.on_message(filters.media_group)
async def album_handler(client, message):
    await handle_album(client, message)

@app.on_message(filters.document | filters.video | filters.photo | filters.audio)
async def file_handler(client, message):
    await handle_single_file(client, message)

def run():
    print("🚀 Monospace Caption Bot is running...")
    app.run()
