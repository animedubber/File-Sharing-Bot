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

# Force Channels Functions
async def get_force_channels():
    try:
        doc = force_channels_col.find_one({"_id": "channels"})
        return doc.get("channel_list", []) if doc else []
    except Exception as e:
        LOGGER(__name__).error(f"Error getting force channels: {e}")
        return []

async def add_force_channel(channel_id):
    try:
        channels = await get_force_channels()
        if channel_id not in channels:
            channels.append(channel_id)
            force_channels_col.update_one(
                {"_id": "channels"},
                {"$set": {"channel_list": channels}},
                upsert=True
            )
            return True
        return False
    except Exception as e:
        LOGGER(__name__).error(f"Error adding force channel: {e}")
        return False

async def remove_force_channel(channel_id):
    try:
        channels = await get_force_channels()
        if channel_id in channels:
            channels.remove(channel_id)
            force_channels_col.update_one(
                {"_id": "channels"},
                {"$set": {"channel_list": channels}},
                upsert=True
            )
            return True
        return False
    except Exception as e:
        LOGGER(__name__).error(f"Error removing force channel: {e}")
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