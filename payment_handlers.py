"""
Payment-related handlers for the BGMI Tournament Bot
"""

import logging
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user, create_payment_request, get_active_tournaments, get_tournament
from config import *
from utils.helpers import is_valid_utr

logger = logging.getLogger(__name__)

async def paid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /paid command"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ Please start the bot first using /start")
        return
    
    # Check if user has pending payments
    active_tournaments = get_active_tournaments()
    if not active_tournaments:
        await update.message.reply_text("❌ No active tournaments available for payment.")
        return
    
    # Check if user is already in tournament participants
    user_tournaments = [t for t in active_tournaments if user_id in t.get('participants', [])]
    
    if user_tournaments:
        text = f"""💰 **Payment Submission**

You are registered for these tournaments:
"""
        for tournament in user_tournaments:
            text += f"🎮 {tournament['name']}\n"
            text += f"💵 Entry Fee: ₹{tournament['entry_fee']}\n\n"
        
        text += f"""**Payment Details:**
💳 UPI ID: `{UPI_ID}`
📱 Send screenshot to: {ADMIN_USERNAME}

**After payment:**
1. Send screenshot to admin
2. Reply to this message with your UTR number
3. Wait for admin confirmation

**Please enter your UTR number:**"""
        
        # Set user state for UTR input
        context.user_data["awaiting_utr"] = True
        context.user_data["payment_tournaments"] = [t["tournament_id"] for t in user_tournaments]
        
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text("""❌ You are not registered for any tournaments.

Please join a tournament first before making payment.""")

async def process_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process UTR number input"""
    user_id = update.effective_user.id
    
    # Check if user is in UTR input state
    if not context.user_data.get("awaiting_utr"):
        return  # Ignore if not waiting for UTR
    
    utr_number = update.message.text.strip()
    
    # Basic UTR validation
    if not is_valid_utr(utr_number):
        await update.message.reply_text("""❌ Invalid UTR number format.

UTR should be 12 digits. Please check and try again.
Example: 123456789012""")
        return
    
    # Get tournament IDs from user data
    tournament_ids = context.user_data.get("payment_tournaments", [])
    
    if not tournament_ids:
        await update.message.reply_text("❌ No tournaments found for payment.")
        return
    
    # Create payment requests for all tournaments
    success_count = 0
    for tournament_id in tournament_ids:
        tournament = get_tournament(tournament_id)
        if tournament:
            payment_id = create_payment_request(
                user_id=user_id,
                tournament_id=tournament_id,
                amount=tournament["entry_fee"],
                utr_number=utr_number
            )
            if payment_id:
                success_count += 1
    
    if success_count > 0:
        # Clear user state
        context.user_data["awaiting_utr"] = False
        context.user_data["payment_tournaments"] = []
        
        confirmation_text = f"""✅ **Payment Submitted Successfully!**

📝 **UTR Number:** `{utr_number}`
🎮 **Tournaments:** {success_count}
⏰ **Submitted:** {datetime.now(pytz.timezone(TIMEZONE)).strftime('%d/%m/%Y %H:%M IST')}

**Next Steps:**
1. Screenshot sent to {ADMIN_USERNAME} ✅
2. UTR submitted ✅
3. Waiting for admin confirmation ⏳

**Admin will confirm within 30 minutes.**
You'll receive a notification once confirmed.

**Payment Details for Reference:**
💳 UPI ID: `{UPI_ID}`
📱 Admin: {ADMIN_USERNAME}"""
        
        keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data="main_menu")]]
        
        await update.message.reply_text(
            confirmation_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Notify admin about new payment
        admin_notification = f"""💰 **New Payment Submission**

👤 **User:** {update.effective_user.first_name} (@{update.effective_user.username or 'No username'})
🆔 **User ID:** `{user_id}`
📝 **UTR:** `{utr_number}`
🎮 **Tournaments:** {success_count}
⏰ **Time:** {datetime.now(pytz.timezone(TIMEZONE)).strftime('%d/%m/%Y %H:%M IST')}

Use `/confirm @{update.effective_user.username or user_id}` to approve
Use `/decline @{update.effective_user.username or user_id}` to decline"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=admin_notification,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Failed to notify admin: {e}")
    else:
        await update.message.reply_text("❌ Failed to submit payment. Please try again or contact support.")
