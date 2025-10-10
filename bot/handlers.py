import logging
from pyrogram import Client
from pyrogram.types import Message, InputMediaPhoto, InputMediaDocument, InputMediaVideo, InputMediaAudio
from .utils import to_monospace

logger = logging.getLogger(__name__)

async def handle_single_file(client: Client, message: Message):
    # Skip if this message is part of a media group (album)
    if getattr(message, "media_group_id", None):
        return
    caption = message.caption or ""
    # Do not reply if there's no caption to convert
    if not caption.strip():
        return
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
    except Exception as e:
        logger.error(f"Error processing file: {e}")


async def handle_album(client: Client, message: Message):
    media_group_id = message.media_group_id
    if not media_group_id:
        return

    messages = await client.get_media_group(message.chat.id, media_group_id)
    
    # Only process if this is the first message in the group (lowest ID)
    if message.id != min(msg.id for msg in messages):
        return
        
    caption = messages[0].caption or ""
    # Do not send an album reply if no caption provided
    if not caption.strip():
        return
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

    if not media:
        return

    try:
        await client.send_media_group(chat_id=message.chat.id, media=media)
    except Exception as e:
        logger.error(f"Error processing media group: {e}")
