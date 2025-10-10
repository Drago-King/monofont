import logging
from pyrogram import Client, filters
from config.settings import API_ID, API_HASH, BOT_TOKEN, LOG_LEVEL, validate_config
from .handlers import handle_single_file, handle_album

# Configure logging from environment
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = Client(
    "monospace_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.media_group)
async def album_handler(client, message):
    await handle_album(client, message)

@app.on_message(filters.document | filters.video | filters.photo | filters.audio)
async def file_handler(client, message):
    await handle_single_file(client, message)

def run():
    validate_config()
    app.run()
