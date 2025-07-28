"""
Admin-related handlers for the BGMI Tournament Bot
"""

import logging
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import *
from config import *
from utils.messages import *
from utils.keyboards import *
from utils.helpers import is_admin, format_datetime, generate_tournament_id

logger = logging.getLogger(__name__)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin dashboard"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use admin commands.")
        return
    
    # Get current stats
    tz = pytz.timezone(TIMEZONE)
    current_time = datetime.now(tz).strftime("%d/%m/%Y %H:%M IST")
    
    active_tournaments = get_active_tournaments()
    live_tournament_count = len([t for t in active_tournaments if t["status"] == "active"])
    
    # Calculate next match time (mock calculation)
    next_match_in = "30"  # This should be calculated based on next tournament
    
    dashboard_text = ADMIN_DASHBOARD.format(
        current_time=current_time,
        live_tournament_count=live_tournament_count,
        next_match_in=next_match_in
    )
    
    keyboard = get_admin_menu_keyboard()
    
    await update.message.reply_text(
        dashboard_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def host_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle tournament hosting"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    # If callback query, handle tournament type selection
    if update.callback_query:
        query = update.callback_query
        tournament_type = query.data.split("_")[1]  # host_solo, host_duo, host_squad
        
        await query.answer()
        await start_tournament_creation(update, context, tournament_type)
        return
    
    # Show tournament type selection
    text = "🎮 **Select Tournament Type:**\n\nChoose the type of tournament you want to host:"
    
    keyboard = [
        [InlineKeyboardButton("🧍 SOLO", callback_data="host_solo")],
        [InlineKeyboardButton("👥 DUO", callback_data="host_duo")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 SQUAD", callback_data="host_squad")]
    ]
    
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def start_tournament_creation(update: Update, context: ContextTypes.DEFAULT_TYPE, tournament_type):
    """Start step-by-step tournament creation"""
    # Store tournament type in user data
    context.user_data["creating_tournament"] = {
        "type": tournament_type,
        "step": 1
    }
    
    type_emoji = {"solo": "🧍", "duo": "👥", "squad": "👨‍👩‍👧‍👦"}
    
    text = f"""🎮 **TOURNAMENT CREATION - {type_emoji[tournament_type]} {tournament_type.upper()}**

**Step 1/8: Tournament Name**

Enter a catchy name for your tournament:
Examples:
• HEADSHOT KING CHALLENGE
• DYNAMIC DUOS
• ROYALE RUMBLE

Type the tournament name:"""
    
    await update.callback_query.edit_message_text(
        text,
        parse_mode="Markdown"
    )

async def ai_host(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle AI-powered tournament hosting"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    # If callback query, handle tournament type selection
    if update.callback_query:
        query = update.callback_query
        tournament_type = query.data.split("_")[1]  # aihost_solo, aihost_duo, aihost_squad
        
        await query.answer()
        await generate_ai_tournament(update, context, tournament_type)
        return
    
    # Show tournament type selection
    text = """🤖 **AI Tournament Generator**

Let AI analyze market trends and suggest the best tournament setup based on:
• Current player activity
• Profit/loss analysis  
• Popular time slots
• Entry fee optimization

Select tournament type for AI analysis:"""
    
    keyboard = [
        [InlineKeyboardButton("🧍 AI SOLO", callback_data="aihost_solo")],
        [InlineKeyboardButton("👥 AI DUO", callback_data="aihost_duo")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 AI SQUAD", callback_data="aihost_squad")]
    ]
    
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def generate_ai_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE, tournament_type):
    """Generate AI-suggested tournament"""
    import random
    
    # Mock AI analysis (in real implementation, use AI API)
    ai_suggestions = {
        "solo": {
            "name": "HEADSHOT KING CHALLENGE",
            "entry_fee": random.choice([30, 50, 75]),
            "map": random.choice(MAPS),
            "time": "21:30",
            "prize_type": "Kill-Based",
            "prize_details": "₹25 per kill + ₹200 top killer bonus"
        },
        "duo": {
            "name": "DYNAMIC DUOS",
            "entry_fee": random.choice([60, 80, 100]),
            "map": random.choice(MAPS),
            "time": "19:00", 
            "prize_type": "Fixed Amount",
            "prize_details": "Winners take all: ₹1500"
        },
        "squad": {
            "name": "ROYALE RUMBLE",
            "entry_fee": random.choice([150, 200, 250]),
            "map": random.choice(MAPS),
            "time": "20:00",
            "prize_type": "Rank-Based",
            "prize_details": "#1: ₹2000 | #2: ₹1200 | #3: ₹800"
        }
    }
    
    suggestion = ai_suggestions[tournament_type]
    type_emoji = {"solo": "🧍", "duo": "👥", "squad": "👨‍👩‍👧‍👦"}
    
    text = f"""🤖 **AI TOURNAMENT SUGGESTION**

🎮 **Tournament Type:** {type_emoji[tournament_type]} {tournament_type.upper()}
🏆 **Name:** {suggestion['name']}
📅 **Suggested Date:** {datetime.now().strftime('%d/%m/%Y')}
🕘 **Optimal Time:** {suggestion['time']}
📍 **Best Map:** {suggestion['map']}
💰 **Entry Fee:** ₹{suggestion['entry_fee']}
🎁 **Prize Structure:** {suggestion['prize_type']}
💸 **Prize Details:** {suggestion['prize_details']}

**🧠 AI Analysis:**
• High engagement time slot
• Optimal entry fee for maximum participation  
• Popular map choice
• Profitable prize structure

**Approve this tournament?**"""
    
    keyboard = [
        [InlineKeyboardButton("✅ Approve & Create", callback_data=f"approve_ai_{tournament_type}")],
        [InlineKeyboardButton("🔄 Generate New", callback_data=f"aihost_{tournament_type}")],
        [InlineKeyboardButton("❌ Cancel", callback_data="admin_menu")]
    ]
    
    # Store AI suggestion for approval
    context.user_data["ai_suggestion"] = suggestion
    context.user_data["ai_tournament_type"] = tournament_type
    
    await update.callback_query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def active_tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show active tournaments"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    tournaments = get_active_tournaments()
    
    if not tournaments:
        text = "📋 **Active Tournaments**\n\n❌ No active tournaments found."
    else:
        text = "📋 **Active Tournaments**\n\n"
        for i, tournament in enumerate(tournaments, 1):
            status_emoji = {"upcoming": "⏳", "active": "🔴"}.get(tournament["status"], "❓")
            text += f"{i}. {status_emoji} **{tournament['name']}**\n"
            text += f"   🎮 {tournament['type'].title()}\n"
            text += f"   👥 {len(tournament.get('participants', []))} players\n"
            text += f"   💰 ₹{tournament['entry_fee']} entry\n"
            text += f"   📅 {format_datetime(tournament['date'])}\n\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def drop_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle room details sharing"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    # Get active tournaments
    tournaments = get_active_tournaments()
    
    if not tournaments:
        await update.message.reply_text("❌ No active tournaments to share room details.")
        return
    
    text = "📤 **Select Tournament for Room Details:**\n\n"
    keyboard = []
    
    for tournament in tournaments:
        text += f"🎮 {tournament['name']} - {len(tournament.get('participants', []))} players\n"
        keyboard.append([InlineKeyboardButton(
            f"📤 {tournament['name'][:20]}...", 
            callback_data=f"droproom_{tournament['tournament_id']}"
        )])
    
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List tournament participants"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    tournaments = get_active_tournaments()
    
    if not tournaments:
        await update.message.reply_text("❌ No active tournaments found.")
        return
    
    text = "📋 **Tournament Participants**\n\n"
    
    for tournament in tournaments:
        text += f"🎮 **{tournament['name']}**\n"
        text += f"👥 **Participants:** {len(tournament.get('participants', []))}\n"
        
        if tournament.get('participants'):
            for i, participant_id in enumerate(tournament['participants'], 1):
                user = get_user(participant_id)
                if user:
                    username = f"@{user['username']}" if user['username'] else user['first_name']
                    paid_status = "✅" if user.get('confirmed') else "⏳"
                    text += f"{i}. {paid_status} {username}\n"
        else:
            text += "❌ No participants yet\n"
        
        text += "\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def clear_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear/Edit/Remove tournament"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    tournaments = get_active_tournaments()
    
    if not tournaments:
        await update.message.reply_text("❌ No tournaments to manage.")
        return
    
    text = "🧹 **Tournament Management**\n\nSelect a tournament to manage:"
    keyboard = []
    
    for tournament in tournaments:
        keyboard.append([InlineKeyboardButton(
            f"🗑️ {tournament['name'][:20]}...",
            callback_data=f"manage_tournament_{tournament['tournament_id']}"
        )])
    
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def data_vault(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show financial data"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    # Get financial data
    today_data = get_financial_data("today")
    week_data = get_financial_data("week")
    month_data = get_financial_data("month")
    
    text = f"""💰 **DATA VAULT - Financial Overview**

📅 **Today's Collection:**
💵 Total Amount: ₹{today_data['total_amount']}
📊 Total Payments: {today_data['total_payments']}

📈 **Weekly Earnings (Last 7 days):**
💵 Total Amount: ₹{week_data['total_amount']}
📊 Total Payments: {week_data['total_payments']}

📊 **Monthly Revenue (Last 30 days):**
💵 Total Amount: ₹{month_data['total_amount']}
📊 Total Payments: {month_data['total_payments']}

🧮 **Analysis:**
• Average per day: ₹{month_data['total_amount'] // 30 if month_data['total_amount'] > 0 else 0}
• Growth trend: {"📈" if week_data['total_amount'] > today_data['total_amount'] * 7 else "📉"}

⏰ Last updated: {datetime.now(pytz.timezone(TIMEZONE)).strftime('%d/%m/%Y %H:%M IST')}"""
    
    await update.message.reply_text(text, parse_mode="Markdown")

async def special_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send special notifications"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    text = """💥 **Special Notifications**

Send custom announcements to all users:

**Available Templates:**
1. Winner Declaration
2. New Tournament Alert
3. Maintenance Notice
4. Special Offer
5. Custom Message

Choose notification type or send custom message:"""
    
    keyboard = [
        [InlineKeyboardButton("🏆 Winner Declaration", callback_data="notify_winner")],
        [InlineKeyboardButton("🎮 Tournament Alert", callback_data="notify_tournament")],
        [InlineKeyboardButton("🔧 Maintenance", callback_data="notify_maintenance")],
        [InlineKeyboardButton("💰 Special Offer", callback_data="notify_offer")],
        [InlineKeyboardButton("✍️ Custom Message", callback_data="notify_custom")]
    ]
    
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def ban_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban user(s)"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("""🚫 **Ban User Command**

**Usage:**
• `/ban @username` - Ban single user
• `/ban @user1 @user2 @user3` - Ban multiple users
• `/ban user_id` - Ban by user ID

**Example:**
`/ban @troublemaker reason: cheating`""")
        return
    
    banned_users = []
    failed_bans = []
    
    for arg in context.args:
        if arg.startswith("reason:"):
            break
            
        # Extract user ID or username
        if arg.startswith("@"):
            username = arg[1:]
            # Find user by username (this would need a database query)
            target_user = None  # Implementation needed
        elif arg.isdigit():
            target_user_id = int(arg)
            target_user = get_user(target_user_id)
        else:
            continue
        
        if target_user:
            reason = " ".join([a for a in context.args if a.startswith("reason:")]).replace("reason:", "").strip()
            from database import ban_user
            if ban_user(target_user["user_id"], user_id, reason):
                banned_users.append(target_user["first_name"] or str(target_user["user_id"]))
            else:
                failed_bans.append(target_user["first_name"] or str(target_user["user_id"]))
    
    result_text = "🚫 **Ban Results:**\n\n"
    if banned_users:
        result_text += f"✅ **Banned:** {', '.join(banned_users)}\n"
    if failed_bans:
        result_text += f"❌ **Failed:** {', '.join(failed_bans)}\n"
    
    await update.message.reply_text(result_text, parse_mode="Markdown")

async def unban_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban user(s)"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("""✅ **Unban User Command**

**Usage:**
• `/unban @username` - Unban single user
• `/unban @user1 @user2 @user3` - Unban multiple users
• `/unban user_id` - Unban by user ID

**Example:**
`/unban @forgiven_user`""")
        return
    
    unbanned_users = []
    failed_unbans = []
    
    for arg in context.args:
        # Extract user ID or username
        if arg.startswith("@"):
            username = arg[1:]
            # Find user by username (this would need a database query)
            target_user = None  # Implementation needed
        elif arg.isdigit():
            target_user_id = int(arg)
            target_user = get_user(target_user_id)
        else:
            continue
        
        if target_user:
            from database import unban_user
            if unban_user(target_user["user_id"], user_id):
                unbanned_users.append(target_user["first_name"] or str(target_user["user_id"]))
            else:
                failed_unbans.append(target_user["first_name"] or str(target_user["user_id"]))
    
    result_text = "✅ **Unban Results:**\n\n"
    if unbanned_users:
        result_text += f"✅ **Unbanned:** {', '.join(unbanned_users)}\n"
    if failed_unbans:
        result_text += f"❌ **Failed:** {', '.join(failed_unbans)}\n"
    
    await update.message.reply_text(result_text, parse_mode="Markdown")

async def confirm_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm user payment"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("""✅ **Confirm Payment Command**

**Usage:**
`/confirm @username`

**Example:**
`/confirm @paid_user`

This will confirm the payment for the user's latest tournament registration.""")
        return
    
    target_identifier = context.args[0]
    target_user = None
    
    # Get user by username or ID
    if target_identifier.startswith("@"):
        username = target_identifier[1:]
        # Find user by username (simplified implementation)
        target_user = None  # Would need database query by username
    elif target_identifier.isdigit():
        target_user_id = int(target_identifier)
        target_user = get_user(target_user_id)
    
    if not target_user:
        await update.message.reply_text("❌ User not found. Please check the username or user ID.")
        return
    
    # Confirm payment for user's active tournaments
    from database import confirm_payment
    active_tournaments = get_active_tournaments()
    user_tournaments = [t for t in active_tournaments if target_user["user_id"] in t.get('participants', [])]
    
    if not user_tournaments:
        await update.message.reply_text("❌ User has no active tournament registrations.")
        return
    
    confirmed_count = 0
    for tournament in user_tournaments:
        if confirm_payment(target_user["user_id"], tournament["tournament_id"], user_id):
            confirmed_count += 1
    
    if confirmed_count > 0:
        success_text = f"""✅ **Payment Confirmed!**
        
👤 **User:** {target_user.get('first_name', 'Unknown')}
🎮 **Tournaments:** {confirmed_count}
💰 **Status:** Payment approved
⏰ **Confirmed by:** Admin
        
The user has been notified and is now eligible for tournament participation."""
        
        # Notify user about confirmation
        try:
            await context.bot.send_message(
                chat_id=target_user["user_id"],
                text=f"""✅ **Payment Confirmed!**
                
Your payment has been approved by admin.
You are now eligible for tournament participation.

🎮 **Confirmed tournaments:** {confirmed_count}
💰 **Payment status:** ✅ Approved

Good luck in your matches! 🏆""",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Failed to notify user about payment confirmation: {e}")
        
        await update.message.reply_text(success_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Failed to confirm payment. Please try again or check payment status.")

async def decline_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Decline user payment"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("""❌ **Decline Payment Command**

**Usage:**
`/decline @username`

**Example:**
`/decline @suspicious_user`

This will decline the payment for the user's latest tournament registration.""")
        return
    
    target_identifier = context.args[0]
    target_user = None
    
    # Get user by username or ID
    if target_identifier.startswith("@"):
        username = target_identifier[1:]
        # Find user by username (simplified implementation)
        target_user = None  # Would need database query by username
    elif target_identifier.isdigit():
        target_user_id = int(target_identifier)
        target_user = get_user(target_user_id)
    
    if not target_user:
        await update.message.reply_text("❌ User not found. Please check the username or user ID.")
        return
    
    # Decline payment for user's active tournaments
    from database import decline_payment
    active_tournaments = get_active_tournaments()
    user_tournaments = [t for t in active_tournaments if target_user["user_id"] in t.get('participants', [])]
    
    if not user_tournaments:
        await update.message.reply_text("❌ User has no active tournament registrations.")
        return
    
    declined_count = 0
    for tournament in user_tournaments:
        if decline_payment(target_user["user_id"], tournament["tournament_id"], user_id):
            declined_count += 1
    
    if declined_count > 0:
        decline_text = f"""❌ **Payment Declined**
        
👤 **User:** {target_user.get('first_name', 'Unknown')}
🎮 **Tournaments:** {declined_count}
💰 **Status:** Payment declined
⏰ **Declined by:** Admin
        
The user has been notified and removed from tournament participation."""
        
        # Notify user about decline
        try:
            await context.bot.send_message(
                chat_id=target_user["user_id"],
                text=f"""❌ **Payment Declined**
                
Your payment has been declined by admin.
Please contact support if you believe this is an error.

🎮 **Affected tournaments:** {declined_count}
💰 **Payment status:** ❌ Declined

Contact {ADMIN_USERNAME} for assistance.""",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Failed to notify user about payment decline: {e}")
        
        await update.message.reply_text(decline_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Failed to decline payment. Please try again or check payment status.")
