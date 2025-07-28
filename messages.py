"""
Message templates for the BGMI Tournament Bot
"""

from config import *

# Tournament creation messages
TOURNAMENT_CREATION_STEPS = {
    "solo": {
        1: "**Step 1/8: Tournament Name**\nEnter a catchy name for SOLO tournament:",
        2: "**Step 2/8: Date**\nEnter tournament date (DD/MM/YYYY):",
        3: "**Step 3/8: Time**\nEnter tournament time (HH:MM format, 24h):",
        4: "**Step 4/8: Map**\nSelect the map for the tournament:",
        5: "**Step 5/8: Entry Fee**\nEnter entry fee amount (₹):",
        6: "**Step 6/8: Prize Type**\nSelect prize distribution type:",
        7: "**Step 7/8: Prize Details**\nEnter prize details:",
        8: "**Step 8/8: Confirmation**\nReview your tournament details:"
    },
    "duo": {
        1: "**Step 1/8: Tournament Name**\nEnter a catchy name for DUO tournament:",
        2: "**Step 2/8: Date**\nEnter tournament date (DD/MM/YYYY):",
        3: "**Step 3/8: Time**\nEnter tournament time (HH:MM format, 24h):",
        4: "**Step 4/8: Map**\nSelect the map for the tournament:",
        5: "**Step 5/8: Entry Fee**\nEnter entry fee per team (₹):",
        6: "**Step 6/8: Prize Type**\nSelect prize distribution type:",
        7: "**Step 7/8: Prize Details**\nEnter prize details:",
        8: "**Step 8/8: Confirmation**\nReview your tournament details:"
    },
    "squad": {
        1: "**Step 1/8: Tournament Name**\nEnter a catchy name for SQUAD tournament:",
        2: "**Step 2/8: Date**\nEnter tournament date (DD/MM/YYYY):",
        3: "**Step 3/8: Time**\nEnter tournament time (HH:MM format, 24h):",
        4: "**Step 4/8: Map**\nSelect the map for the tournament:",
        5: "**Step 5/8: Entry Fee**\nEnter entry fee per squad (₹):",
        6: "**Step 6/8: Prize Type**\nSelect prize distribution type:",
        7: "**Step 7/8: Prize Details**\nEnter prize details:",
        8: "**Step 8/8: Confirmation**\nReview your tournament details:"
    }
}

TOURNAMENT_POST_TEMPLATE = """🎮 **TOURNAMENT ALERT**

🏆 **{name}**
📅 **Date:** {date}
🕘 **Time:** {time}
📍 **Map:** {map}
💰 **Entry Fee:** ₹{entry_fee}
🎁 **Prize Pool:** {prize_details}
👥 **Type:** {tournament_type}

👇 **Click to Join**"""

ROOM_DETAILS_TEMPLATE = """🚪 **ROOM DETAILS DROPPED!**

🎮 **Tournament:** {tournament_name}
🆔 **Room ID:** `{room_id}`
🔐 **Password:** `{password}`
📍 **Map:** {map}
⏰ **Match Time:** {time}

**⚠️ Important Instructions:**
1. Join room 10 minutes before match time
2. Set your in-game name as registered
3. No late entries allowed
4. Wait for admin to start the match

**🎯 All the best, legends!**
May the best squad win! 🏆

**Problems?** Contact {admin_username}"""

WINNER_ANNOUNCEMENT_TEMPLATE = """🏆 **WINNER ANNOUNCEMENT**

🎮 **Tournament:** {tournament_name}
📅 **Date:** {date}

**🥇 CHAMPIONS:**
{winners_list}

**🎁 Prize Distribution:**
{prize_distribution}

**📊 Match Stats:**
• Total Participants: {total_participants}
• Total Kills: {total_kills}
• Duration: {match_duration}

**💰 Prizes will be credited within 24 hours**

**🎯 Thank you all for participating!**
Join our next tournament for more action! 🔥

{admin_username} | {channel_url}"""

PAYMENT_REMINDER_TEMPLATE = """⏰ **Payment Reminder**

🎮 **Tournament:** {tournament_name}
⏳ **Time Left:** {time_left}

**💳 Payment Required:**
💰 Amount: ₹{amount}
🆔 UPI ID: `{upi_id}`

**⚠️ Warning:**
Room details will be shared in {time_left}.
Unpaid participants will be removed!

**Quick Steps:**
1. Pay now to UPI
2. Send screenshot to {admin_username}
3. Use /paid command with UTR

**Don't miss out! 🔥**"""

BAN_NOTIFICATION_TEMPLATE = """🚫 **Account Banned**

Your account has been banned from No Mercy Zone.

**Reason:** {reason}
**Date:** {ban_date}
**Admin:** {admin_username}

**Appeal:**
Contact {support_email} with your case details.

**Note:** Multiple violations result in permanent bans."""

WELCOME_BACK_TEMPLATE = """✅ **Welcome Back!**

Your account has been unbanned and restored.

**Unbanned by:** {admin_username}
**Date:** {unban_date}

You can now participate in tournaments again.
Please follow all rules to avoid future issues.

**Happy Gaming! 🎮**"""

ERROR_MESSAGES = {
    "not_started": "❌ Please start the bot first using /start",
    "banned": "❌ You are banned from using this bot.",
    "not_member": "❌ You must join our channel first to use the bot.",
    "no_tournaments": "❌ No active tournaments available.",
    "already_joined": "✅ You are already registered for this tournament!",
    "tournament_full": "❌ This tournament is full. Try joining the next one!",
    "payment_required": "💰 Payment is required to complete your registration.",
    "invalid_utr": "❌ Invalid UTR number. Please check and try again.",
    "admin_only": "❌ This command is for admins only.",
    "tournament_not_found": "❌ Tournament not found.",
    "user_not_found": "❌ User not found.",
    "database_error": "❌ Database error. Please try again later.",
    "invalid_format": "❌ Invalid format. Please check your input.",
    "tournament_ended": "❌ This tournament has already ended.",
    "room_already_shared": "❌ Room details have already been shared for this tournament."
}

SUCCESS_MESSAGES = {
    "tournament_created": "✅ Tournament created successfully!",
    "payment_confirmed": "✅ Payment confirmed! You are now eligible for the tournament.",
    "user_banned": "✅ User has been banned successfully.",
    "user_unbanned": "✅ User has been unbanned successfully.",
    "tournament_deleted": "✅ Tournament deleted successfully.",
    "room_shared": "✅ Room details have been shared with all participants.",
    "notification_sent": "✅ Notification sent to all users."
}
