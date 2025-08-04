
from pyrogram import Client
from pyrogram.types import BotCommand
from bot import Bot
from config import LOGGER

@Bot.on_message()
async def set_bot_commands(client: Client, message):
    """Set bot commands menu - this runs once when bot starts"""
    if hasattr(client, 'commands_set'):
        return
    
    commands = [
        BotCommand("start", "Start the bot or get posts"),
        BotCommand("batch", "Create link for multiple posts"),
        BotCommand("genlink", "Create link for one post"),
        BotCommand("id", "Check user ID"),
        BotCommand("users", "View bot statistics (Admin only)"),
        BotCommand("broadcast", "Broadcast messages to users (Admin only)"),
        BotCommand("stats", "Check bot uptime (Admin only)"),
    ]
    
    try:
        await client.set_bot_commands(commands)
        client.commands_set = True
        LOGGER(__name__).info("Bot commands menu has been set successfully!")
    except Exception as e:
        LOGGER(__name__).error(f"Failed to set bot commands: {e}")
