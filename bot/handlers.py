import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from .utils import to_monospace

logger = logging.getLogger(__name__)

async def handle_single_file(client: Client, message: Message):
    caption = message.caption or ""
    new_caption = to_monospace(caption)

    try:
        if message.document:
            await message.reply_document(
                document=message.document.file_id,
                caption=new_caption,
                parse_mode="MarkdownV2"
            )
        elif message.photo:
            await message.reply_photo(
                photo=message.photo.file_id,
                caption=new_caption,
                parse_mode="MarkdownV2"
            )
        elif message.video:
            await message.reply_video(
                video=message.video.file_id,
                caption=new_caption,
                parse_mode="MarkdownV2"
            )
        elif message.audio:
            await message.reply_audio(
                audio=message.audio.file_id,
                caption=new_caption,
                parse_mode="MarkdownV2"
            )
        logger.info(f"Processed file from user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        await message.reply_text("❌ Failed to process your file.")


async def handle_album(client: Client, message: Message):
    media_group_id = message.media_group_id
    if not media_group_id:
        return

    messages = await client.get_media_group(message.chat.id, media_group_id)
    caption = messages[0].caption or ""
    new_caption = to_monospace(caption)

    media = []
    for msg in messages:
        if msg.photo:
            media.append({"type": "photo", "media": msg.photo.file_id})
        elif msg.document:
            media.append({"type": "document", "media": msg.document.file_id})
        elif msg.video:
            media.append({"type": "video", "media": msg.video.file_id})

    try:
        await client.send_media_group(chat_id=message.chat.id, media=media, caption=new_caption)
        logger.info(f"Processed media group from user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error processing media group: {e}")
        await message.reply_text("❌ Failed to process your media group.")
