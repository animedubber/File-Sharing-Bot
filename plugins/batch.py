
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

@Bot.on_message(filters.command('batch') & filters.user(ADMINS))
async def batch_command(client: Bot, message: Message):
    """Generate batch links for multiple messages"""
    while True:
        try:
            first_message = await client.ask(text="Forward the First Message from DB Channel (with /cancel to cancel)", chat_id=message.from_user.id, timeout=60.0)
        except:
            return
        if first_message.text and first_message.text.startswith('/cancel'):
            return await first_message.reply('Cancelled!')
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nThis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    while True:
        try:
            second_message = await client.ask(text="Forward the Last Message from DB Channel (with /cancel to cancel)", chat_id=message.from_user.id, timeout=60.0)
        except:
            return
        if second_message.text and second_message.text.startswith('/cancel'):
            return await second_message.reply('Cancelled!')
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nThis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = None
    await second_message.reply_text(f"<b>📦 Here is your Batch Link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True, quote=True)
