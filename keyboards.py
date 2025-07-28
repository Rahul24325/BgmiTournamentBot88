"""
Keyboard layouts for the BGMI Tournament Bot
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import MAPS

def get_main_menu_keyboard():
    """Main menu keyboard"""
    return [
        [InlineKeyboardButton("🎮 Active Tournament", callback_data="active_tournaments")],
        [InlineKeyboardButton("📜 Terms & Condition", callback_data="terms_conditions")],
        [InlineKeyboardButton("👥 Invite Friends", callback_data="invite_friends")],
        [InlineKeyboardButton("📱 Share WhatsApp Status", callback_data="share_whatsapp")],
        [InlineKeyboardButton("📜 Match History", callback_data="match_history")],
        [InlineKeyboardButton("🆘 Help", callback_data="help")]
    ]

def get_admin_menu_keyboard():
    """Admin menu keyboard"""
    return [
        [InlineKeyboardButton("🎮 Host Tournament", callback_data="host_menu")],
        [InlineKeyboardButton("🤖 AI Host", callback_data="aihost_menu")],
        [InlineKeyboardButton("📋 Active Tournaments", callback_data="admin_active")],
        [InlineKeyboardButton("📤 Drop Room", callback_data="admin_droproom")],
        [InlineKeyboardButton("👥 List Players", callback_data="admin_listplayers")],
        [InlineKeyboardButton("🧹 Clear Tournament", callback_data="admin_clear")],
        [InlineKeyboardButton("💰 Data Vault", callback_data="admin_datavault")],
        [InlineKeyboardButton("💥 Special Notification", callback_data="admin_special")],
        [InlineKeyboardButton("🚫 Ban/Unban", callback_data="admin_ban_menu")]
    ]

def get_tournament_type_keyboard():
    """Tournament type selection keyboard"""
    return [
        [InlineKeyboardButton("🧍 SOLO", callback_data="host_solo")],
        [InlineKeyboardButton("👥 DUO", callback_data="host_duo")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 SQUAD", callback_data="host_squad")]
    ]

def get_ai_tournament_type_keyboard():
    """AI tournament type selection keyboard"""
    return [
        [InlineKeyboardButton("🧍 AI SOLO", callback_data="aihost_solo")],
        [InlineKeyboardButton("👥 AI DUO", callback_data="aihost_duo")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 AI SQUAD", callback_data="aihost_squad")]
    ]

def get_map_selection_keyboard():
    """Map selection keyboard"""
    keyboard = []
    for i in range(0, len(MAPS), 2):
        row = []
        row.append(InlineKeyboardButton(f"📍 {MAPS[i]}", callback_data=f"map_{MAPS[i].lower()}"))
        if i + 1 < len(MAPS):
            row.append(InlineKeyboardButton(f"📍 {MAPS[i+1]}", callback_data=f"map_{MAPS[i+1].lower()}"))
        keyboard.append(row)
    return keyboard

def get_prize_type_keyboard():
    """Prize type selection keyboard"""
    return [
        [InlineKeyboardButton("💀 Kill-Based", callback_data="prize_kill")],
        [InlineKeyboardButton("💰 Fixed Amount", callback_data="prize_fixed")],
        [InlineKeyboardButton("🏆 Rank-Based", callback_data="prize_rank")]
    ]

def get_tournament_actions_keyboard(tournament_id):
    """Tournament action buttons"""
    return [
        [InlineKeyboardButton("✅ Join Now", callback_data=f"join_tournament_{tournament_id}")],
        [InlineKeyboardButton("📜 Rules", callback_data=f"tournament_rules_{tournament_id}")],
        [InlineKeyboardButton("⚠️ Disclaimer", callback_data=f"tournament_disclaimer_{tournament_id}")]
    ]

def get_tournament_management_keyboard(tournament_id):
    """Tournament management keyboard for admins"""
    return [
        [InlineKeyboardButton("📤 Share Room", callback_data=f"share_room_{tournament_id}")],
        [InlineKeyboardButton("👥 View Players", callback_data=f"view_players_{tournament_id}")],
        [InlineKeyboardButton("✏️ Edit Tournament", callback_data=f"edit_tournament_{tournament_id}")],
        [InlineKeyboardButton("🗑️ Delete Tournament", callback_data=f"delete_tournament_{tournament_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data="admin_menu")]
    ]

def get_payment_keyboard(tournament_id, entry_fee):
    """Payment options keyboard"""
    return [
        [InlineKeyboardButton("💰 Pay via UPI", url=f"upi://pay?pa=8435010927@ybl&am={entry_fee}")],
        [InlineKeyboardButton("📱 Contact Admin", url="https://t.me/Ghost_Commander")],
        [InlineKeyboardButton("📜 Payment Guide", callback_data=f"payment_guide_{tournament_id}")]
    ]

def get_confirmation_keyboard(action_type, item_id):
    """Confirmation dialog keyboard"""
    return [
        [InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{action_type}_{item_id}")],
        [InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{action_type}_{item_id}")]
    ]

def get_ban_management_keyboard():
    """Ban management keyboard"""
    return [
        [InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban_user")],
        [InlineKeyboardButton("✅ Unban User", callback_data="admin_unban_user")],
        [InlineKeyboardButton("📋 Banned Users", callback_data="admin_banned_list")],
        [InlineKeyboardButton("🔙 Back", callback_data="admin_menu")]
    ]

def get_notification_type_keyboard():
    """Notification type selection keyboard"""
    return [
        [InlineKeyboardButton("🏆 Winner Declaration", callback_data="notify_winner")],
        [InlineKeyboardButton("🎮 Tournament Alert", callback_data="notify_tournament")],
        [InlineKeyboardButton("🔧 Maintenance Notice", callback_data="notify_maintenance")],
        [InlineKeyboardButton("💰 Special Offer", callback_data="notify_offer")],
        [InlineKeyboardButton("✍️ Custom Message", callback_data="notify_custom")]
    ]

def get_back_to_menu_keyboard():
    """Simple back to menu keyboard"""
    return [[InlineKeyboardButton("🏠 Back to Menu", callback_data="main_menu")]]

def get_entry_fee_suggestions_keyboard():
    """Entry fee suggestion keyboard"""
    return [
        [InlineKeyboardButton("₹30", callback_data="fee_30"), InlineKeyboardButton("₹50", callback_data="fee_50")],
        [InlineKeyboardButton("₹75", callback_data="fee_75"), InlineKeyboardButton("₹100", callback_data="fee_100")],
        [InlineKeyboardButton("₹150", callback_data="fee_150"), InlineKeyboardButton("₹200", callback_data="fee_200")],
        [InlineKeyboardButton("✍️ Custom Amount", callback_data="fee_custom")]
    ]

def get_time_suggestions_keyboard():
    """Time suggestion keyboard"""
    return [
        [InlineKeyboardButton("🌅 09:00", callback_data="time_09:00"), InlineKeyboardButton("🌄 12:00", callback_data="time_12:00")],
        [InlineKeyboardButton("🌆 18:00", callback_data="time_18:00"), InlineKeyboardButton("🌃 21:00", callback_data="time_21:00")],
        [InlineKeyboardButton("🌙 22:30", callback_data="time_22:30"), InlineKeyboardButton("✍️ Custom", callback_data="time_custom")]
    ]

def get_active_tournaments_keyboard(tournaments):
    """Active tournaments list keyboard"""
    keyboard = []
    for tournament in tournaments:
        keyboard.append([InlineKeyboardButton(
            f"🎮 {tournament['name'][:25]}{'...' if len(tournament['name']) > 25 else ''}",
            callback_data=f"view_tournament_{tournament['tournament_id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")])
    return keyboard
