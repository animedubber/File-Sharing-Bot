from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id
import asyncio


@Bot.on_message(filters.command('batch') & filters.user(ADMINS))
async def batch_link_generator(client: Bot, message: Message):
    """Generate batch links for multiple posts"""

    if message.reply_to_message:
        replied = message.reply_to_message
        msg_id = await get_message_id(client, replied)
        if msg_id:
            base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
            link = f"https://t.me/{client.username}?start={base64_string}"
            reply_markup = None
            await message.reply_text(
                f"<b>🔗 Here is your link:</b>\n\n{link}",
                quote=True,
                reply_markup=reply_markup
            )
        else:
            await message.reply_text("❌ This message is not from the DB channel", quote=True)
    else:
        await message.reply_text(
            "**Usage:**\n"
            "Reply to a message from the DB channel to generate batch link\n\n"
            "**Example:**\n"
            "Reply to a forwarded message with `/batch`"
        )


@Bot.on_message(filters.command('genlink') & filters.user(ADMINS))
async def single_link_generator(client: Bot, message: Message):
    """Generate single post links"""

    if message.reply_to_message:
        replied = message.reply_to_message
        msg_id = await get_message_id(client, replied)
        if msg_id:
            base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
            link = f"https://t.me/{client.username}?start={base64_string}"
            reply_markup = None
            await message.reply_text(
                f"<b>🔗 Here is your link:</b>\n\n{link}",
                quote=True,
                reply_markup=reply_markup
            )
        else:
            await message.reply_text("❌ This message is not from the DB channel", quote=True)
    else:
        await message.reply_text(
            "**Usage:**\n"
            "Reply to a message from the DB channel to generate single link\n\n"
            "**Example:**\n"
            "Reply to a forwarded message with `/genlink`"
        )


# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper