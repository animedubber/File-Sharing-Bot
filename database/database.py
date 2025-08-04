import pymongo, os
from config import DB_URL, DB_NAME, LOGGER

dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]
user_data = database['users']
settings_col = database["bot_settings"]
force_channels_col = database["force_channels"]



async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])

    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

# Bot Settings Functions
async def get_bot_settings():
    try:
        settings = settings_col.find_one({"_id": "bot_config"})
        return settings or {}
    except Exception as e:
        LOGGER(__name__).error(f"Error getting bot settings: {e}")
        return {}

async def update_bot_settings(key, value):
    try:
        settings_col.update_one(
            {"_id": "bot_config"},
            {"$set": {key: value}},
            upsert=True
        )
        return True
    except Exception as e:
        LOGGER(__name__).error(f"Error updating bot settings: {e}")
        return False

# Force Channels Functions with types
async def get_force_channels():
    try:
        doc = force_channels_col.find_one({"_id": "channels"})
        if not doc:
            return []
        
        # Handle old format (list) and new format (dict with types)
        channels_data = doc.get("channel_list", [])
        if isinstance(channels_data, list):
            # Convert old format to new format
            return [{"id": ch, "type": "normal"} for ch in channels_data]
        else:
            return channels_data
    except Exception as e:
        LOGGER(__name__).error(f"Error getting force channels: {e}")
        return []

async def get_force_channel_ids():
    try:
        channels = await get_force_channels()
        return [ch["id"] if isinstance(ch, dict) else ch for ch in channels]
    except Exception as e:
        LOGGER(__name__).error(f"Error getting force channel IDs: {e}")
        return []

async def add_force_channel(channel_id, channel_type="normal"):
    try:
        channels = await get_force_channels()
        
        # Check if channel already exists
        existing_ids = [ch["id"] if isinstance(ch, dict) else ch for ch in channels]
        if channel_id in existing_ids:
            return False
            
        # Add new channel with type
        new_channel = {"id": channel_id, "type": channel_type}
        channels.append(new_channel)
        
        force_channels_col.update_one(
            {"_id": "channels"},
            {"$set": {"channel_list": channels}},
            upsert=True
        )
        return True
    except Exception as e:
        LOGGER(__name__).error(f"Error adding force channel: {e}")
        return False

async def remove_force_channel(channel_id):
    try:
        channels = await get_force_channels()
        updated_channels = []
        
        for ch in channels:
            ch_id = ch["id"] if isinstance(ch, dict) else ch
            if ch_id != channel_id:
                updated_channels.append(ch)
        
        force_channels_col.update_one(
            {"_id": "channels"},
            {"$set": {"channel_list": updated_channels}},
            upsert=True
        )
        return True
    except Exception as e:
        LOGGER(__name__).error(f"Error removing force channel: {e}")
        return False

async def update_channel_type(channel_id, new_type):
    try:
        channels = await get_force_channels()
        updated = False
        
        for ch in channels:
            if isinstance(ch, dict) and ch["id"] == channel_id:
                ch["type"] = new_type
                updated = True
                break
        
        if updated:
            force_channels_col.update_one(
                {"_id": "channels"},
                {"$set": {"channel_list": channels}},
                upsert=True
            )
        
        return updated
    except Exception as e:
        LOGGER(__name__).error(f"Error updating channel type: {e}")
        return False

async def update_auto_delete_time(seconds):
    try:
        return await update_bot_settings("auto_delete_time", seconds)
    except Exception as e:
        LOGGER(__name__).error(f"Error updating auto delete time: {e}")
        return False









# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper