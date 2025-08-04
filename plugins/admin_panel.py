
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import Bot
from config import ADMINS, OWNER_ID, FORCE_SUB_CHANNELS, FILE_AUTO_DELETE
from database.database import get_bot_settings, update_bot_settings, add_force_channel, remove_force_channel, get_force_channels, update_auto_delete_time
import re

@Bot.on_message(filters.command('admin') & filters.private & filters.user(ADMINS))
async def admin_panel(client: Bot, message: Message):
    user_id = message.from_user.id
    is_owner = user_id == OWNER_ID
    
    buttons = [
        [InlineKeyboardButton("⚙️ Bot Settings", callback_data="admin_settings")],
        [InlineKeyboardButton("📢 Force Channels", callback_data="admin_force_channels")],
        [InlineKeyboardButton("⏰ Auto Delete", callback_data="admin_auto_delete")],
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
    ]
    
    if is_owner:
        buttons.append([InlineKeyboardButton("👥 Manage Admins", callback_data="admin_manage_admins")])
    
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close")])
    
    await message.reply_text(
        f"<b>🛠️ Admin Panel</b>\n\n"
        f"Welcome {message.from_user.mention}!\n"
        f"Role: {'Owner' if is_owner else 'Admin'}\n\n"
        f"Select an option to manage bot settings:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Bot.on_callback_query(filters.regex(r"^admin_"))
async def admin_callback_handler(client: Bot, query: CallbackQuery):
    user_id = query.from_user.id
    is_owner = user_id == OWNER_ID
    data = query.data
    
    if user_id not in ADMINS:
        await query.answer("❌ Access denied!", show_alert=True)
        return
    
    if data == "admin_settings":
        settings = await get_bot_settings()
        text = f"""<b>⚙️ Bot Settings</b>

<b>Current Settings:</b>
• Start Message: {'Custom' if settings.get('custom_start_msg') else 'Default'}
• Force Sub Message: {'Custom' if settings.get('custom_force_msg') else 'Default'}
• Protect Content: {'✅ Enabled' if settings.get('protect_content', True) else '❌ Disabled'}
• Channel Button: {'❌ Disabled' if settings.get('disable_channel_button', False) else '✅ Enabled'}

<b>Actions:</b>"""
        
        buttons = [
            [InlineKeyboardButton("📝 Set Start Message", callback_data="admin_set_start_msg")],
            [InlineKeyboardButton("📢 Set Force Message", callback_data="admin_set_force_msg")],
            [InlineKeyboardButton("🔒 Toggle Content Protection", callback_data="admin_toggle_protect")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_back")]
        ]
        
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    
    elif data == "admin_force_channels":
        channels = await get_force_channels()
        text = f"<b>📢 Force Subscription Channels</b>\n\n"
        
        if channels:
            text += "<b>Active Channels:</b>\n"
            for i, channel_id in enumerate(channels, 1):
                try:
                    chat = await client.get_chat(channel_id)
                    name = chat.title or chat.first_name
                    text += f"{i}. {name} (<code>{channel_id}</code>)\n"
                except:
                    text += f"{i}. Unknown Channel (<code>{channel_id}</code>)\n"
        else:
            text += "❌ No force channels configured"
        
        buttons = [
            [InlineKeyboardButton("➕ Add Channel", callback_data="admin_add_channel")],
        ]
        
        if channels:
            buttons.append([InlineKeyboardButton("➖ Remove Channel", callback_data="admin_remove_channel")])
        
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="admin_back")])
        
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    
    elif data == "admin_auto_delete":
        settings = await get_bot_settings()
        current_time = settings.get('auto_delete_time', FILE_AUTO_DELETE)
        
        hours = current_time // 3600
        minutes = (current_time % 3600) // 60
        seconds = current_time % 60
        
        time_str = ""
        if hours > 0:
            time_str += f"{hours}h "
        if minutes > 0:
            time_str += f"{minutes}m "
        if seconds > 0:
            time_str += f"{seconds}s"
        
        text = f"""<b>⏰ Auto Delete Settings</b>

<b>Current Auto Delete Time:</b> {time_str.strip() or '0s'}

<b>Quick Settings:</b>"""
        
        buttons = [
            [
                InlineKeyboardButton("5m", callback_data="admin_set_delete_300"),
                InlineKeyboardButton("10m", callback_data="admin_set_delete_600"),
                InlineKeyboardButton("30m", callback_data="admin_set_delete_1800")
            ],
            [
                InlineKeyboardButton("1h", callback_data="admin_set_delete_3600"),
                InlineKeyboardButton("6h", callback_data="admin_set_delete_21600"),
                InlineKeyboardButton("24h", callback_data="admin_set_delete_86400")
            ],
            [InlineKeyboardButton("🔧 Custom Time", callback_data="admin_custom_delete")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_back")]
        ]
        
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    
    elif data.startswith("admin_set_delete_"):
        delete_time = int(data.split("_")[-1])
        await update_auto_delete_time(delete_time)
        await query.answer(f"✅ Auto delete time updated to {delete_time} seconds!", show_alert=True)
        await admin_callback_handler(client, CallbackQuery(
            id=query.id, from_user=query.from_user, chat_instance=query.chat_instance,
            message=query.message, data="admin_auto_delete"
        ))
    
    elif data == "admin_back":
        await admin_panel(client, query.message)

@Bot.on_message(filters.text & filters.private & filters.user(ADMINS), group=10)
async def handle_admin_input(client: Bot, message: Message):
    # Handle admin inputs for various settings
    if hasattr(client, 'awaiting_input') and message.from_user.id in client.awaiting_input:
        input_type = client.awaiting_input[message.from_user.id]
        
        if input_type == "add_channel":
            channel_input = message.text.strip()
            
            # Try to extract channel ID from various formats
            channel_id = None
            if channel_input.startswith('@'):
                try:
                    chat = await client.get_chat(channel_input)
                    channel_id = chat.id
                except:
                    await message.reply("❌ Channel not found or bot is not admin in the channel!")
                    return
            elif channel_input.startswith('-100') or channel_input.startswith('-'):
                try:
                    channel_id = int(channel_input)
                except:
                    await message.reply("❌ Invalid channel ID format!")
                    return
            else:
                await message.reply("❌ Please provide a valid channel ID (e.g., -1001234567890) or username (e.g., @channel)")
                return
            
            # Verify bot is admin in the channel
            try:
                chat_member = await client.get_chat_member(channel_id, client.me.id)
                if chat_member.status not in ['administrator', 'creator']:
                    await message.reply("❌ Bot must be admin in the channel!")
                    return
            except:
                await message.reply("❌ Cannot access channel or bot is not admin!")
                return
            
            # Add channel to database
            success = await add_force_channel(channel_id)
            if success:
                chat = await client.get_chat(channel_id)
                await message.reply(f"✅ Channel '{chat.title}' added successfully!")
            else:
                await message.reply("❌ Channel already exists or error occurred!")
            
            del client.awaiting_input[message.from_user.id]
        
        elif input_type == "remove_channel":
            try:
                channel_id = int(message.text.strip())
                success = await remove_force_channel(channel_id)
                if success:
                    await message.reply("✅ Channel removed successfully!")
                else:
                    await message.reply("❌ Channel not found!")
            except:
                await message.reply("❌ Please provide a valid channel ID!")
            
            del client.awaiting_input[message.from_user.id]
        
        elif input_type == "custom_delete_time":
            try:
                # Parse time input (supports formats like: 30m, 1h, 2h30m, 3600s, etc.)
                time_str = message.text.strip().lower()
                total_seconds = parse_time_string(time_str)
                
                if total_seconds <= 0:
                    await message.reply("❌ Invalid time format! Use formats like: 30m, 1h, 2h30m, 3600s")
                    return
                
                await update_auto_delete_time(total_seconds)
                await message.reply(f"✅ Auto delete time set to {total_seconds} seconds!")
            except:
                await message.reply("❌ Invalid time format! Use formats like: 30m, 1h, 2h30m, 3600s")
            
            del client.awaiting_input[message.from_user.id]

@Bot.on_callback_query(filters.regex(r"^admin_(add_channel|remove_channel|custom_delete)$"))
async def admin_input_callback(client: Bot, query: CallbackQuery):
    if not hasattr(client, 'awaiting_input'):
        client.awaiting_input = {}
    
    data = query.data
    user_id = query.from_user.id
    
    if data == "admin_add_channel":
        client.awaiting_input[user_id] = "add_channel"
        await query.message.edit_text(
            "<b>➕ Add Force Channel</b>\n\n"
            "Send the channel ID or username:\n"
            "• Channel ID: <code>-1001234567890</code>\n"
            "• Username: <code>@channelname</code>\n\n"
            "⚠️ Make sure the bot is admin in the channel!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel", callback_data="admin_force_channels")]
            ])
        )
    
    elif data == "admin_remove_channel":
        channels = await get_force_channels()
        if not channels:
            await query.answer("❌ No channels to remove!", show_alert=True)
            return
        
        text = "<b>➖ Remove Force Channel</b>\n\nActive channels:\n"
        for i, channel_id in enumerate(channels, 1):
            try:
                chat = await client.get_chat(channel_id)
                name = chat.title or chat.first_name
                text += f"{i}. {name} - <code>{channel_id}</code>\n"
            except:
                text += f"{i}. Unknown Channel - <code>{channel_id}</code>\n"
        
        text += "\nSend the channel ID to remove:"
        
        client.awaiting_input[user_id] = "remove_channel"
        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel", callback_data="admin_force_channels")]
            ])
        )
    
    elif data == "admin_custom_delete":
        client.awaiting_input[user_id] = "custom_delete_time"
        await query.message.edit_text(
            "<b>🔧 Custom Auto Delete Time</b>\n\n"
            "Send the time in one of these formats:\n"
            "• <code>30s</code> - 30 seconds\n"
            "• <code>5m</code> - 5 minutes\n"
            "• <code>2h</code> - 2 hours\n"
            "• <code>1h30m</code> - 1 hour 30 minutes\n"
            "• <code>3600</code> - 3600 seconds\n",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel", callback_data="admin_auto_delete")]
            ])
        )

def parse_time_string(time_str):
    """Parse time string and return total seconds"""
    total_seconds = 0
    
    # If it's just a number, treat as seconds
    if time_str.isdigit():
        return int(time_str)
    
    # Parse hour, minute, second patterns
    hour_match = re.search(r'(\d+)h', time_str)
    minute_match = re.search(r'(\d+)m', time_str)
    second_match = re.search(r'(\d+)s', time_str)
    
    if hour_match:
        total_seconds += int(hour_match.group(1)) * 3600
    if minute_match:
        total_seconds += int(minute_match.group(1)) * 60
    if second_match:
        total_seconds += int(second_match.group(1))
    
    return total_seconds
