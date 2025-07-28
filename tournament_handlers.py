"""
Tournament-related handlers for the BGMI Tournament Bot
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_tournament, join_tournament as db_join_tournament, get_user, is_user_banned
from config import *
from utils.helpers import format_datetime

logger = logging.getLogger(__name__)

async def join_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle tournament joining"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    tournament_id = query.data.split("_")[2]  # join_tournament_123
    
    # Check if user is banned
    if is_user_banned(user_id):
        await query.edit_message_text("❌ You are banned from joining tournaments.")
        return
    
    # Get tournament details
    tournament = get_tournament(tournament_id)
    if not tournament:
        await query.edit_message_text("❌ Tournament not found.")
        return
    
    # Check if tournament is still accepting participants
    if tournament["status"] != "upcoming":
        await query.edit_message_text("❌ This tournament is no longer accepting participants.")
        return
    
    # Check if user is already joined
    if user_id in tournament.get("participants", []):
        await query.edit_message_text("✅ You are already registered for this tournament!")
        return
    
    # Join tournament
    success = db_join_tournament(user_id, tournament_id)
    
    if success:
        # Get user details
        user = get_user(user_id)
        
        success_text = f"""✅ **Successfully Joined Tournament!**

🎮 **Tournament:** {tournament['name']}
📅 **Date:** {format_datetime(tournament['date'])}
🕘 **Time:** {tournament['time']}
📍 **Map:** {tournament['map']}
💰 **Entry Fee:** ₹{tournament['entry_fee']}

**💳 Payment Required:**
1. Pay ₹{tournament['entry_fee']} to UPI: `{UPI_ID}`
2. Send screenshot to {ADMIN_USERNAME}
3. Use /paid command with UTR number
4. Wait for confirmation

**⚠️ Important:**
• Payment must be completed before room details are shared
• No refunds after room details are distributed
• Be punctual for the match

**Next Steps:**
1. Make payment ₹{tournament['entry_fee']} ⏳
2. Send proof to admin ⏳
3. Submit UTR via /paid ⏳
4. Get confirmation ⏳"""
        
        keyboard = [
            [InlineKeyboardButton("💰 Make Payment", url=f"upi://pay?pa={UPI_ID}&am={tournament['entry_fee']}")],
            [InlineKeyboardButton("📜 Rules", callback_data=f"tournament_rules_{tournament_id}")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            success_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.edit_message_text("❌ Failed to join tournament. Please try again.")

async def tournament_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show tournament rules"""
    query = update.callback_query
    await query.answer()
    
    tournament_id = query.data.split("_")[2]  # tournament_rules_123
    tournament = get_tournament(tournament_id)
    
    if not tournament:
        await query.edit_message_text("❌ Tournament not found.")
        return
    
    rules_text = f"""📜 **Tournament Rules - {tournament['name']}**

**🎮 General Rules:**
1. ✅ No emulators allowed (mobile devices only)
2. ✅ No teaming with opponents
3. ✅ No hacking/cheating tools
4. ✅ Kill + Rank = Final points calculation
5. ✅ Be punctual - room closes 5 min after start time

**📱 Device Requirements:**
• Mobile phone/tablet only
• Stable internet connection
• Latest BGMI version installed

**🎯 Scoring System:**
• Each kill = Points
• Final rank = Bonus points
• Combination determines winner

**⚠️ Violations:**
• Emulator use = Immediate disqualification
• Teaming = Ban from future tournaments  
• Cheating = Permanent account ban
• Late joining = Forfeit entry fee

**🏆 Prize Distribution:**
• Winners announced within 2 hours
• Prizes credited within 24 hours
• Screenshot proof required for claims

**📞 Support:**
Contact {ADMIN_USERNAME} for any queries during the match."""
    
    keyboard = [
        [InlineKeyboardButton("⚠️ Disclaimer", callback_data=f"tournament_disclaimer_{tournament_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"join_tournament_{tournament_id}")]
    ]
    
    await query.edit_message_text(
        rules_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def tournament_disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show tournament disclaimer"""
    query = update.callback_query
    await query.answer()
    
    tournament_id = query.data.split("_")[2]  # tournament_disclaimer_123
    tournament = get_tournament(tournament_id)
    
    if not tournament:
        await query.edit_message_text("❌ Tournament not found.")
        return
    
    disclaimer_text = f"""⚠️ **Tournament Disclaimer - {tournament['name']}**

**🚫 No Refund Policy:**
• Entry fees are non-refundable once room details are shared
• Technical issues on player's end don't qualify for refunds
• Tournament cancellation by organizer = full refund

**📱 Technical Responsibility:**
• We are not responsible for:
  - Internet connection issues
  - Device lag or performance
  - BGMI server downtime
  - Power outages during match

**🎮 Fair Play:**
• All participants play at their own risk
• Decisions by admin/moderator are final
• No arguments accepted post-match
• Evidence required for any complaints

**💰 Prize Claims:**
• Winners must provide valid proof
• Prizes subject to verification
• False claims result in permanent ban
• Payment processing may take 24-48 hours

**📞 Disputes:**
• Report issues during match only
• Post-match complaints not entertained
• Admin decisions are final and binding
• Contact {ADMIN_USERNAME} for urgent issues

**✅ Agreement:**
By joining this tournament, you accept all terms and conditions mentioned above.

**🎯 Play Fair, Win Big!**"""
    
    keyboard = [
        [InlineKeyboardButton("📜 Rules", callback_data=f"tournament_rules_{tournament_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"join_tournament_{tournament_id}")]
    ]
    
    await query.edit_message_text(
        disclaimer_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
