
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot


@Bot.on_message(filters.command('id'))
async def get_id(client: Client, message: Message):
    """Get user ID command"""
    if message.reply_to_message:
        if message.reply_to_message.forward_from:
            user_id = message.reply_to_message.forward_from.id
            first_name = message.reply_to_message.forward_from.first_name
            await message.reply_text(
                f"<b>User ID:</b> <code>{user_id}</code>\n<b>Name:</b> {first_name}"
            )
        else:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
            await message.reply_text(
                f"<b>User ID:</b> <code>{user_id}</code>\n<b>Name:</b> {first_name}"
            )
    else:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        await message.reply_text(
            f"<b>Your ID:</b> <code>{user_id}</code>\n<b>Name:</b> {first_name}"
        )


# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
