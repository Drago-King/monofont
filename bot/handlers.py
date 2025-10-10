import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto, InputMediaDocument, InputMediaVideo, InputMediaAudio
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
    
    # Only process if this is the first message in the group (lowest ID)
    if message.id != min(msg.id for msg in messages):
        return
        
    caption = messages[0].caption or ""
    new_caption = to_monospace(caption)

    media = []
    for idx, msg in enumerate(messages):
        is_first = idx == 0
        if msg.photo:
            media_item = InputMediaPhoto(
                media=msg.photo.file_id,
                caption=new_caption if is_first else None,
                parse_mode="MarkdownV2" if is_first else None
            )
            media.append(media_item)
        elif msg.document:
            media_item = InputMediaDocument(
                media=msg.document.file_id,
                caption=new_caption if is_first else None,
                parse_mode="MarkdownV2" if is_first else None
            )
            media.append(media_item)
        elif msg.video:
            media_item = InputMediaVideo(
                media=msg.video.file_id,
                caption=new_caption if is_first else None,
                parse_mode="MarkdownV2" if is_first else None
            )
            media.append(media_item)
        elif msg.audio:
            media_item = InputMediaAudio(
                media=msg.audio.file_id,
                caption=new_caption if is_first else None,
                parse_mode="MarkdownV2" if is_first else None
            )
            media.append(media_item)

    try:
        await client.send_media_group(chat_id=message.chat.id, media=media)
        logger.info(f"Processed media group from user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error processing media group: {e}")
        await message.reply_text("❌ Failed to process your media group.")
