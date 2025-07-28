"""
User-related handlers for the BGMI Tournament Bot
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from database import get_user, create_user, generate_referral_code, get_user_match_history, is_user_banned
from config import *
from utils.messages import *
from utils.keyboards import *
from utils.helpers import check_channel_membership, format_datetime

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Check if user is admin
    if user.id == ADMIN_ID:
        from handlers.admin_handlers import admin_panel
        await admin_panel(update, context)
        return
    
    # Check if user is banned
    if is_user_banned(user.id):
        await update.message.reply_text("❌ You are banned from using this bot.")
        return
    
    # Get or create user
    db_user = get_user(user.id)
    if not db_user:
        # Generate referral code
        referral_code = generate_referral_code(user.id)
        
        # Create new user
        user_data = {
            "user_id": user.id,
            "username": user.username or "",
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "referral_code": referral_code,
            "referred_by": None,
            "paid": False,
            "confirmed": False
        }
        
        # Check if referred by someone
        if context.args and context.args[0].startswith("REF"):
            referrer = get_user_by_referral_code(context.args[0])
            if referrer:
                user_data["referred_by"] = referrer["user_id"]
        
        create_user(user_data)
        db_user = get_user(user.id)
    
    # Send welcome message
    welcome_text = WELCOME_MESSAGE.format(
        name=user.first_name,
        support_email=SUPPORT_EMAIL,
        instagram=INSTAGRAM_HANDLE,
        admin_username=ADMIN_USERNAME,
        channel_url=CHANNEL_URL
    )
    
    await update.message.reply_text(welcome_text)
    
    # Check channel membership
    await check_membership(update, context)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if user joined the channel"""
    user_id = update.effective_user.id
    
    # Check channel membership
    is_member = await check_channel_membership(context.bot, user_id, CHANNEL_ID)
    
    if not is_member:
        keyboard = [
            [InlineKeyboardButton("✅ Join Channel", url=CHANNEL_URL)],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_membership")]
        ]
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                FORCE_JOIN_MESSAGE,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text(
                FORCE_JOIN_MESSAGE,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return
    
    # User is member, show main menu
    await show_menu(update, context)

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu"""
    user = update.effective_user
    db_user = get_user(user.id)
    
    menu_text = MENU_MESSAGE.format(
        name=user.first_name,
        referral_code=db_user["referral_code"]
    )
    
    keyboard = get_main_menu_keyboard()
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            menu_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            menu_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def invite_friends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle invite friends"""
    user = update.effective_user
    db_user = get_user(user.id)
    
    referral_code = db_user["referral_code"]
    referral_link = f"https://t.me/KyaTereSquadMeinDumHaiBot?start={referral_code}"
    
    whatsapp_status = WHATSAPP_STATUS.format(referral_code=referral_code)
    
    invite_text = f"""👥 **Invite Friends & Earn FREE ENTRY!**

📱 **Your Referral Link:**
`{referral_link}`

📢 **WhatsApp Status (Copy & Share):**
{whatsapp_status}

**How it works:**
1. Share your referral link with friends
2. When they join using your code, you earn credits
3. Use credits for FREE tournament entry!

**Benefits:**
🔥 FREE tournament entries
💰 Bonus rewards for active referrers
🏆 VIP access to special tournaments

**Start sharing and start winning!**"""
    
    keyboard = get_back_to_menu_keyboard()
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            invite_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            invite_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def match_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's match history"""
    user_id = update.effective_user.id
    
    if is_user_banned(user_id):
        await update.message.reply_text("❌ You are banned from using this bot.")
        return
    
    history = get_user_match_history(user_id)
    
    if not history:
        text = """📜 **Match History**

❌ No match history found.
Join your first tournament to see your stats here!

**What you'll see here:**
• Tournament participation
• Your performance stats
• Prize winnings
• Match dates and results"""
    else:
        text = "📜 **Your Match History**\n\n"
        for i, match in enumerate(history, 1):
            status_emoji = {"upcoming": "⏳", "active": "🔴", "completed": "✅"}.get(match.get("status"), "❓")
            text += f"{i}. {status_emoji} **{match['name']}**\n"
            text += f"   📅 {format_datetime(match['date'])}\n"
            text += f"   🎮 {match['type'].title()}\n\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information"""
    help_text = f"""🆘 **Help & Support**

**🎮 Tournament Commands:**
• `/start` - Start the bot and register
• `/paid` - Submit payment after joining tournament
• `/matchhistory` - View your tournament history

**👥 User Features:**
• Join active tournaments
• Invite friends for rewards  
• Track match history
• View rules and disclaimers

**💰 Payment Process:**
1. Join a tournament
2. Pay entry fee to UPI: `{UPI_ID}`
3. Send screenshot to {ADMIN_USERNAME}
4. Use `/paid` with UTR number
5. Wait for confirmation

**📞 Support:**
📧 Email: {SUPPORT_EMAIL}
👤 Admin: {ADMIN_USERNAME}
📸 Instagram: {INSTAGRAM_HANDLE}
🔗 Channel: {CHANNEL_URL}
💬 Discussion: {DISCUSSION_GROUP_URL}

**🎯 Happy Gaming!**
Join tournaments, play fair, and win big! 🏆"""
    
    await update.message.reply_text(help_text, parse_mode="Markdown")

def get_user_by_referral_code(referral_code):
    """Get user by referral code"""
    from database import db
    try:
        return db.users.find_one({"referral_code": referral_code})
    except Exception as e:
        logger.error(f"Error getting user by referral code: {e}")
        return None

async def show_active_tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show active tournaments"""
    from database import get_active_tournaments
    from utils.keyboards import get_tournament_actions_keyboard
    
    user_id = update.effective_user.id
    
    if is_user_banned(user_id):
        await update.message.reply_text("❌ You are banned from using this bot.")
        return
    
    tournaments = get_active_tournaments()
    
    if not tournaments:
        text = """🎮 **Active Tournaments**

❌ No active tournaments available right now.

**Don't worry!** New tournaments are hosted regularly.
Check back in a few hours or enable notifications to get alerts when new tournaments go live!

**Want to be notified?**
Follow our channel: @NoMercyZoneBG"""
        
        keyboard = get_back_to_menu_keyboard()
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return
    
    # Show tournaments one by one
    for tournament in tournaments:
        type_emoji = {"solo": "🧍", "duo": "👥", "squad": "👨‍👩‍👧‍👦"}
        
        tournament_text = f"""🎮 **TOURNAMENT ALERT**

🏆 **{tournament['name']}**
📅 **Date:** {format_datetime(tournament['date'])}
🕘 **Time:** {tournament['time']}
📍 **Map:** {tournament['map']}
💰 **Entry Fee:** ₹{tournament['entry_fee']}
🎁 **Prize Pool:** {tournament.get('prize_details', 'TBD')}
👥 **Type:** {type_emoji.get(tournament['type'], '🎮')} {tournament['type'].title()}
👥 **Participants:** {len(tournament.get('participants', []))}

👇 **Click to Join**"""
        
        keyboard = get_tournament_actions_keyboard(tournament['tournament_id'])
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                tournament_text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text(
                tournament_text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        break  # Show only first tournament, user can navigate

async def show_terms_conditions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show terms and conditions"""
    terms_text = f"""📜 **Terms & Conditions**

**🎮 Tournament Participation:**
1. Must be 16+ years old to participate
2. Only mobile devices allowed (no emulators)
3. Stable internet connection required
4. Latest BGMI version must be installed

**💰 Payment Terms:**
1. Entry fees are non-refundable once room details are shared
2. Payment must be completed before tournament starts
3. UTR number required for payment verification
4. False payment claims result in permanent ban

**🎯 Fair Play Policy:**
1. No hacking, cheating, or third-party tools
2. No teaming with opponents
3. No verbal abuse or toxic behavior
4. Screenshots required for prize claims

**🏆 Prize Distribution:**
1. Prizes credited within 24-48 hours of match completion
2. Valid proof of performance required
3. Disputes must be raised during match only
4. Admin decisions are final and binding

**📱 Data & Privacy:**
1. Telegram username and ID stored for tournament management
2. Payment information kept confidential
3. Match statistics may be shared publicly
4. Users can request data deletion by contacting admin

**⚠️ Violations:**
1. First violation: Warning
2. Second violation: 7-day ban  
3. Third violation: Permanent ban
4. Severe violations: Immediate permanent ban

**📞 Contact:**
Admin: {ADMIN_USERNAME}
Email: {SUPPORT_EMAIL}

By participating, you agree to all terms above."""
    
    keyboard = get_back_to_menu_keyboard()
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            terms_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            terms_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def share_whatsapp_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Share WhatsApp status"""
    user = update.effective_user
    db_user = get_user(user.id)
    
    if not db_user:
        await update.message.reply_text("❌ Please start the bot first using /start")
        return
    
    referral_code = db_user["referral_code"]
    whatsapp_status = WHATSAPP_STATUS.format(referral_code=referral_code)
    
    from utils.helpers import generate_whatsapp_share_url
    share_url = generate_whatsapp_share_url(referral_code)
    
    share_text = f"""📱 **WhatsApp Status Ready!**

Copy the text below and share as your WhatsApp status:

📋 **Status Text:**
```
{whatsapp_status}
```

🔗 **Quick Share Button:**
Click the button below to share directly via WhatsApp!

**Benefits of Sharing:**
🔥 Help friends discover amazing tournaments
💰 Earn referral rewards for each friend who joins
🏆 Build your gaming squad
📈 Grow the No Mercy Zone community"""
    
    keyboard = [
        [InlineKeyboardButton("📱 Share on WhatsApp", url=share_url)],
        [InlineKeyboardButton("🏠 Back to Menu", callback_data="main_menu")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            share_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            share_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
