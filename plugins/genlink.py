
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

@Bot.on_message(filters.command('genlink') & filters.user(ADMINS))
async def genlink_command(client: Bot, message: Message):
    """Generate single message link"""
    while True:
        try:
            forwarded_message = await client.ask(text="Forward Message from the DB Channel (with /cancel to cancel)", chat_id=message.from_user.id, timeout=60.0)
        except:
            return
        if forwarded_message.text and forwarded_message.text.startswith('/cancel'):
            return await forwarded_message.reply('Cancelled!')
        msg_id = await get_message_id(client, forwarded_message)
        if msg_id:
            break
        else:
            await forwarded_message.reply("❌ Error\n\nThis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    string = f"get-{msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = None
    await forwarded_message.reply_text(f"<b>🔗 Here is your Link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True, quote=True)
