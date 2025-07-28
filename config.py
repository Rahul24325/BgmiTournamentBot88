"""
Configuration settings for the BGMI Tournament Bot
"""

import os

# Bot Configuration
BOT_TOKEN = "8341741465:AAG81VWIc84evKwBR1IIbwMoaHQJwgLXLsY"
ADMIN_ID = 5558853984
ADMIN_USERNAME = "@Ghost_Commander"
CHANNEL_ID = -1002880573048
CHANNEL_USERNAME = "@NoMercyZoneBG"
CHANNEL_URL = "https://t.me/NoMercyZoneBG"
DISCUSSION_GROUP_URL = "https://t.me/NoMercyZoneBGG"

# Payment Configuration
UPI_ID = "8435010927@ybl"
SUPPORT_EMAIL = "dumwalasquad.in@zohomail.in"
INSTAGRAM_HANDLE = "@ghostinside.me"

# Database Configuration
MONGODB_URI = "mongodb+srv://rahul7241146384:rahul7241146384@cluster0.qeaogc4.mongodb.net/"
DATABASE_NAME = "nomercyzone_bot"

# AI Configuration
AI_API_KEY = os.getenv("AI_API_KEY", "d96a2478-7fde-4d76-a28d-b8172e561077")

# Tournament Configuration
MAPS = ["Erangel", "Miramar", "Sanhok", "Livik", "Karakin", "Paramo"]
TOURNAMENT_TYPES = ["solo", "duo", "squad"]

# Timezone
TIMEZONE = "Asia/Kolkata"

# Bot Messages
WELCOME_MESSAGE = """🧨 Welcome {name}, the Ghost Commander has arrived!

🚫 This is No Mercy zone! 🔥  
Yahan dosti nahi, bas domination hoti hai 😈  
Squad mein entry ka matlab lobby tera slave ban chuka hai 🕶️

💸 Paisa nahi? Referral bhej aur free entry kama!  
📢 Channel mandatory hai warna winner list se naam gayab!

📧 Support: {support_email}  
📸 Insta: {instagram}  
🎫 {admin_username}  
🔗 Channel: {channel_url}

⚔️ Ghost Commander Squad mein ho ab...  
Ab sirf kills bolenge, baaki sab chup!"""

MENU_MESSAGE = """🔥 Lobby Access Granted! 🔥  
👑 Welcome, {name}.  
🧨 Ab sirf kill karega ya lobby ka malik banega?  
🚫 No Mercy Zone mein sirf legends tikte hain!

Tera Personal Referral Code: `{referral_code}`
Dost ko bhej, aur FREE ENTRY pa!"""

ADMIN_DASHBOARD = """👑 *Welcome Back, 🧨 Ghost Commander!*  
"Server breathe kar raha hai... kyunki Boss wapas aaya hai!" 😎💻

🧨 *System Armed & Ready*  
🕒 *Time:* `{current_time}`  
🎮 *Live Matches:* `{live_tournament_count}`  
🚀 *Next Drop-In:* `{next_match_in} min`

🧬 *Admin Arsenal:* 
Use the commands below to manage your empire!

⚠️ *Note:*  
Yeh teri lobby hai bhai...  
Yahan rules likhta bhi tu hai, todta bhi tu! 🔥🧠"""

FORCE_JOIN_MESSAGE = """❌ Abhi bhi channel join nahi kiya? 
Jaldi se join karo warna entry milegi hi nahi!"""

WHATSAPP_STATUS = """🎮 BGMI TOURNAMENTS LIVE!
🔥 Daily Cash 💰 | 💀 Kill Rewards | 👑 VIP Matches
💥 FREE ENTRY with my code 👉 {referral_code}
📲 Click & Join:
https://t.me/KyaTereSquadMeinDumHaiBot?start={referral_code}
⚡ Limited Slots! Fast join karo!

#BGMI #EarnWithKills"""
