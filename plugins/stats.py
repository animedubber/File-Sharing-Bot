
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS, BOT_STATS_TEXT
from helper_func import get_readable_time
from database.database import full_userbase


@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats_command(client: Client, message: Message):
    """Bot statistics command for admins"""
    users = await full_userbase()
    uptime = get_readable_time((datetime.now() - client.uptime).seconds)
    
    stats_text = f"""<b>📊 Bot Statistics</b>

<b>👥 Total Users:</b> <code>{len(users)}</code>
<b>⏰ Bot Uptime:</b> <code>{uptime}</code>
<b>🤖 Bot Name:</b> <code>{client.me.first_name}</code>
<b>👤 Username:</b> @{client.username}
<b>🆔 Bot ID:</b> <code>{client.me.id}</code>"""
    
    await message.reply_text(stats_text)


# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
