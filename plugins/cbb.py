import os
import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import Bot
from config import ADMINS, BOT_STATS_TEXT
from helper_func import get_readable_time
from database.database import full_userbase


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "close":
        await query.message.delete()

    elif data == "about":
        await query.message.edit_text(
            text=f"""<b>🤖 Bot Name:</b> <code>{client.me.first_name}</code>
<b>👤 Username:</b> @{client.username}
<b>🆔 Bot ID:</b> <code>{client.me.id}</code>
<b>💾 Database:</b> MongoDB
<b>🗃️ Auto Delete:</b> Enabled
<b>👨‍💻 Developer:</b> @JishuDeveloper
<b>📢 Channel:</b> @Madflix_Bots""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
            ])
        )

    elif data == "help":
        await query.message.edit_text(
            text="""<b>📋 Bot Commands:</b>

🚀 <b>/start</b> - Start the bot
📦 <b>/batch</b> - Create batch link for multiple posts
🔗 <b>/genlink</b> - Generate link for single post
🆔 <b>/id</b> - Get your user ID
👥 <b>/users</b> - View bot statistics (Admin only)
📢 <b>/broadcast</b> - Broadcast message to users (Admin only)
📊 <b>/stats</b> - Check bot uptime (Admin only)

<b>📌 How to use:</b>
1. Send files to bot (Admin only)
2. Bot will generate shareable links
3. Share links with users
4. Files auto-delete after specified time""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
            ])
        )

    elif data == "get_id":
        await query.answer(f"Your ID: {query.from_user.id}", show_alert=True)

    elif data == "bot_stats":
        if query.from_user.id in ADMINS:
            users = await full_userbase()
            uptime = get_readable_time((datetime.now() - client.uptime).seconds)
            await query.answer(
                f"📊 Bot Statistics\n\n👥 Total Users: {len(users)}\n⏰ Uptime: {uptime}",
                show_alert=True
            )
        else:
            await query.answer("❌ Admin only feature!", show_alert=True)

    elif data == "batch_help":
        await query.message.edit_text(
            text="""<b>📦 Batch Link Generator</b>

Use <code>/batch</code> command to create links for multiple posts at once.

<b>Steps:</b>
1. Use /batch command
2. Forward multiple messages from DB channel
3. Bot will create a single link for all messages
4. Share the generated link

<b>Note:</b> Only admins can generate batch links.""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
            ])
        )

    elif data == "genlink_help":
        await query.message.edit_text(
            text="""<b>🔗 Single Link Generator</b>

Use <code>/genlink</code> command to create link for a single post.

<b>Steps:</b>
1. Use /genlink command
2. Forward message from DB channel
3. Bot will create a shareable link
4. Share the generated link

<b>Note:</b> Only admins can generate links.""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
            ])
        )

    elif data == "start_back":
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📦 Generate Batch Link", callback_data="batch_help"),
                    InlineKeyboardButton("🔗 Generate Single Link", callback_data="genlink_help")
                ],
                [
                    InlineKeyboardButton("🆔 My ID", callback_data="get_id"),
                    InlineKeyboardButton("📊 Bot Stats", callback_data="bot_stats")
                ],
                [
                    InlineKeyboardButton("😊 About Me", callback_data="about"),
                    InlineKeyboardButton("❓ Help", callback_data="help")
                ],
                [
                    InlineKeyboardButton("🔒 Close", callback_data="close")
                ],
                [
                    InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel_inline")
                ]
            ]
        )

        await query.message.edit_text(
            text=f"""Hello {query.from_user.mention}

I Can Store Private Files In Specified Channel And Other Users Can Access It From Special Link.

🤖 Bot Features:
• Store files securely
• Generate shareable links
• Auto-delete files
• Multi-channel force subscription
• Batch link generation
• Admin controls

Click the buttons below to explore!""",
            reply_markup=reply_markup
        )
    elif data == "admin_panel_inline":
        if query.from_user.id not in ADMINS:
            await query.answer("❌ Access denied!", show_alert=True)
            return

        # Import admin panel function
        from plugins.admin_panel import admin_panel
        
        # Create a mock message object for admin_panel function
        class MockMessage:
            def __init__(self, from_user, chat):
                self.from_user = from_user
                self.chat = chat
                
            async def reply_text(self, text, reply_markup=None):
                await query.message.edit_text(text, reply_markup=reply_markup)
        
        mock_message = MockMessage(query.from_user, query.message.chat)
        await admin_panel(client, mock_message)


# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper