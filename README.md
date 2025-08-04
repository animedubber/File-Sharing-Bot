
# 🤖 File Sharing Bot

A powerful Telegram bot for secure file sharing with auto-delete functionality, multi-channel force subscription, and batch link generation.

![Bot Preview](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSe5yyvpZ2tgx3IkND9JwTSZJpVRZZ0-0LJfA&s)

## ✨ Features

- 🔐 **Secure File Storage** - Store files in private channels
- 🔗 **Link Generation** - Create shareable links for files
- 🗑️ **Auto Delete** - Files automatically delete after specified time
- 📦 **Batch Links** - Generate single link for multiple files
- 🛡️ **4 Force Channels** - Support for up to 4 force subscription channels
- 👥 **User Management** - Track users and broadcast messages
- 🎨 **Custom UI** - Beautiful interface with inline buttons
- 📊 **Statistics** - Admin dashboard with bot statistics
- 🔄 **Auto Deployment** - Easy deployment on Replit

## 🚀 Quick Deploy on Replit

[![Deploy on Replit](https://replit.com/badge/github/JishuDeveloper/File-Sharing-Bot)](https://replit.com/new/github/JishuDeveloper/File-Sharing-Bot)

### Step 1: Fork the Repository
1. Click the "Deploy on Replit" button above
2. Sign in to your Replit account
3. Fork the repository to your account

### Step 2: Set Environment Variables
Go to the **Secrets** tab in Replit and add these variables:

#### Required Variables:
- `BOT_TOKEN` - Get from [@BotFather](https://t.me/BotFather)
- `API_ID` - Get from [my.telegram.org](https://my.telegram.org)
- `API_HASH` - Get from [my.telegram.org](https://my.telegram.org)
- `CHANNEL_ID` - Your database channel ID (make bot admin)
- `OWNER_ID` - Your Telegram user ID
- `DB_URL` - MongoDB connection string
- `DB_NAME` - MongoDB database name

#### Optional Variables:
- `FORCE_SUB_CHANNEL` - First force channel ID (0 to disable)
- `FORCE_SUB_CHANNEL2` - Second force channel ID
- `FORCE_SUB_CHANNEL3` - Third force channel ID  
- `FORCE_SUB_CHANNEL4` - Fourth force channel ID
- `ADMINS` - Admin user IDs (space-separated)
- `FILE_AUTO_DELETE` - Auto delete time in seconds (default: 600)
- `START_PIC` - Start message image URL
- `CUSTOM_CAPTION` - Custom file caption
- `PROTECT_CONTENT` - Enable content protection (True/False)

### Step 3: Setup Channels
1. Create a private channel for database storage
2. Add your bot as admin with all permissions
3. Create force subscription channels (optional)
4. Add bot as admin in force channels with "Invite Users via Link" permission

### Step 4: Deploy
1. Click the **Run** button in Replit
2. Your bot will start automatically
3. The bot is now live and accessible via web interface

## 📱 Bot Commands

### 👥 User Commands:
- `/start` - 🚀 Start the bot or get posts
- `/id` - 🆔 Check your user ID

### 👨‍💻 Admin Commands:
- `/batch` - 📦 Create link for multiple posts  
- `/genlink` - 🔗 Create link for one post
- `/users` - 👥 View bot statistics
- `/broadcast` - 📢 Broadcast messages to users  
- `/stats` - 📊 Check bot uptime

## 🔧 How to Use

### For Users:
1. Start the bot with `/start`
2. Join required channels if force subscription is enabled
3. Use shared links to access files
4. Files will auto-delete after the specified time

### For Admins:
1. Send files directly to the bot to generate links
2. Use `/batch` for multiple file links
3. Use `/genlink` for single file links  
4. Use `/broadcast` to send messages to all users
5. Use `/stats` to view bot statistics

## 🎨 Bot Interface

The bot features a modern interface with:
- 🖼️ **Custom Start Image** - Attractive welcome screen
- 🎛️ **Inline Buttons** - Easy navigation
- 📊 **Statistics Dashboard** - Real-time bot stats
- 💬 **Interactive Callbacks** - Smooth user experience

## 🛠️ Advanced Configuration

### Database Setup:
1. Create a MongoDB database (Free tier available)
2. Get connection string from MongoDB Atlas
3. Add to `DB_URL` variable

### Force Subscription:
```env
FORCE_SUB_CHANNEL=-1001234567890
FORCE_SUB_CHANNEL2=-1001234567891  
FORCE_SUB_CHANNEL3=-1001234567892
FORCE_SUB_CHANNEL4=-1001234567893
```

### Custom Messages:
```env
START_MESSAGE=Welcome {mention}! I can help you share files securely.
FORCE_SUB_MESSAGE=Please join our channels to use the bot.
CUSTOM_CAPTION=📁 {filename}\n\n{previouscaption}
```

## 🔍 Troubleshooting

### Common Issues:

**Bot not starting:**
- Check if all required variables are set
- Verify bot token is correct
- Ensure MongoDB URL is valid

**Force subscription not working:**
- Make sure bot is admin in force channels
- Check channel IDs are correct (include negative sign)
- Verify "Invite Users via Link" permission is enabled

**Files not saving:**
- Ensure bot is admin in database channel
- Check CHANNEL_ID is correct
- Verify channel exists and is accessible

## 📊 MongoDB Setup Guide

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a new cluster
4. Go to Database Access → Add New User
5. Go to Network Access → Add IP (0.0.0.0/0 for global access)
6. Go to Clusters → Connect → Connect Application
7. Copy the connection string and add to `DB_URL`

## 🔒 Security Features

- Content protection to prevent forwarding
- Auto-delete to prevent permanent storage
- Force subscription for access control
- Admin-only file upload
- Secure link generation

## 🤝 Support & Updates

- 📢 **Updates Channel:** [@Madflix_Bots](https://t.me/Madflix_Bots)
- 🆘 **Support Group:** [@MadflixBots_Support](https://t.me/MadflixBots_Support)
- 👨‍💻 **Developer:** [@JishuDeveloper](https://t.me/JishuDeveloper)

## ⭐ Features Coming Soon

- [ ] Multiple database channels support
- [ ] Custom auto-delete times per file
- [ ] File encryption
- [ ] Download statistics
- [ ] User subscription management
- [ ] API integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Developer:** [Jishu Developer](https://github.com/JishuDeveloper)
- **Channel:** [Madflix Bots](https://t.me/Madflix_Bots)
- **Framework:** [Pyrogram](https://github.com/pyrogram/pyrogram)

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

**Made with ❤️ by [Jishu Developer](https://github.com/JishuDeveloper)**

</div>
