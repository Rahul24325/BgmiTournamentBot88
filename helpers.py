"""
Helper functions for the BGMI Tournament Bot
"""

import logging
import re
import pytz
from datetime import datetime, timedelta
from telegram.error import BadRequest
from config import ADMIN_ID, TIMEZONE

logger = logging.getLogger(__name__)

def is_admin(user_id):
    """Check if user is admin"""
    return user_id == ADMIN_ID

async def check_channel_membership(bot, user_id, channel_id):
    """Check if user is member of the channel"""
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except BadRequest:
        logger.error(f"Failed to check membership for user {user_id}")
        return False
    except Exception as e:
        logger.error(f"Error checking channel membership: {e}")
        return False

def is_valid_utr(utr_number):
    """Validate UTR number format"""
    if not utr_number:
        return False
    
    # Remove any spaces or special characters
    utr_clean = re.sub(r'[^0-9]', '', utr_number)
    
    # UTR should be 12 digits
    return len(utr_clean) == 12 and utr_clean.isdigit()

def format_datetime(date_obj):
    """Format datetime object to readable string"""
    if isinstance(date_obj, str):
        # Try to parse string date
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except:
            return date_obj
    
    if date_obj.tzinfo is None:
        date_obj = pytz.timezone(TIMEZONE).localize(date_obj)
    else:
        date_obj = date_obj.astimezone(pytz.timezone(TIMEZONE))
    
    return date_obj.strftime("%d/%m/%Y %H:%M IST")

def parse_date(date_string):
    """Parse date string (DD/MM/YYYY) to datetime object"""
    try:
        return datetime.strptime(date_string, "%d/%m/%Y")
    except ValueError:
        return None

def parse_time(time_string):
    """Parse time string (HH:MM) and validate"""
    try:
        time_obj = datetime.strptime(time_string, "%H:%M").time()
        return time_obj.strftime("%H:%M")
    except ValueError:
        return None

def generate_tournament_id():
    """Generate unique tournament ID"""
    import random
    import string
    
    # Generate 8-character alphanumeric ID
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_room_id():
    """Generate room ID for BGMI"""
    import random
    return str(random.randint(100000, 999999))

def generate_room_password():
    """Generate room password"""
    import random
    import string
    
    # Generate 6-character password with letters and numbers
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def calculate_time_remaining(target_datetime):
    """Calculate time remaining until target datetime"""
    now = datetime.now(pytz.timezone(TIMEZONE))
    
    if isinstance(target_datetime, str):
        target_datetime = datetime.fromisoformat(target_datetime.replace('Z', '+00:00'))
    
    if target_datetime.tzinfo is None:
        target_datetime = pytz.timezone(TIMEZONE).localize(target_datetime)
    else:
        target_datetime = target_datetime.astimezone(pytz.timezone(TIMEZONE))
    
    time_diff = target_datetime - now
    
    if time_diff.total_seconds() <= 0:
        return "Event has started"
    
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def validate_entry_fee(fee_string):
    """Validate and parse entry fee"""
    try:
        fee = int(fee_string.replace('₹', '').replace(',', '').strip())
        if fee < 10:
            return None, "Entry fee must be at least ₹10"
        if fee > 5000:
            return None, "Entry fee cannot exceed ₹5000"
        return fee, None
    except ValueError:
        return None, "Invalid entry fee format"

def format_prize_distribution(prize_type, prize_details):
    """Format prize distribution text"""
    if prize_type == "kill":
        return f"💀 Kill-Based Rewards\n{prize_details}"
    elif prize_type == "fixed":
        return f"💰 Fixed Prize Pool\n{prize_details}"
    elif prize_type == "rank":
        return f"🏆 Rank-Based Distribution\n{prize_details}"
    else:
        return prize_details

def sanitize_input(text):
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove potential harmful characters
    sanitized = re.sub(r'[<>"\']', '', text.strip())
    
    # Limit length
    return sanitized[:200]

def is_valid_username(username):
    """Validate Telegram username format"""
    if not username:
        return False
    
    # Remove @ if present
    username = username.lstrip('@')
    
    # Telegram username rules: 5-32 characters, alphanumeric + underscores
    pattern = r'^[a-zA-Z0-9_]{5,32}$'
    return bool(re.match(pattern, username))

def format_user_mention(user):
    """Format user mention for display"""
    if user.username:
        return f"@{user.username}"
    else:
        return f"{user.first_name} (ID: {user.id})"

def calculate_tournament_stats(tournament):
    """Calculate tournament statistics"""
    participants = tournament.get('participants', [])
    
    stats = {
        'total_participants': len(participants),
        'entry_fee': tournament.get('entry_fee', 0),
        'total_collection': len(participants) * tournament.get('entry_fee', 0),
        'status': tournament.get('status', 'unknown'),
        'created_date': tournament.get('created_at'),
        'tournament_date': tournament.get('date')
    }
    
    return stats

def generate_whatsapp_share_url(referral_code):
    """Generate WhatsApp share URL"""
    message = f"""🎮 BGMI TOURNAMENTS LIVE!
🔥 Daily Cash 💰 | 💀 Kill Rewards | 👑 VIP Matches
💥 FREE ENTRY with my code 👉 {referral_code}
📲 Click & Join:
https://t.me/KyaTereSquadMeinDumHaiBot?start={referral_code}
⚡ Limited Slots! Fast join karo!

#BGMI #EarnWithKills"""
    
    import urllib.parse
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/?text={encoded_message}"

def log_user_action(user_id, action, details=""):
    """Log user actions for analytics"""
    timestamp = datetime.now(pytz.timezone(TIMEZONE)).isoformat()
    logger.info(f"USER_ACTION: {user_id} | {action} | {details} | {timestamp}")

def log_admin_action(admin_id, action, target_id="", details=""):
    """Log admin actions for audit trail"""
    timestamp = datetime.now(pytz.timezone(TIMEZONE)).isoformat()
    logger.info(f"ADMIN_ACTION: {admin_id} | {action} | Target: {target_id} | {details} | {timestamp}")

def is_tournament_time_valid(date_str, time_str):
    """Check if tournament date/time is valid (not in past)"""
    try:
        date_obj = parse_date(date_str)
        time_obj = parse_time(time_str)
        
        if not date_obj or not time_obj:
            return False
        
        # Combine date and time
        tournament_datetime = datetime.combine(date_obj.date(), datetime.strptime(time_obj, "%H:%M").time())
        tournament_datetime = pytz.timezone(TIMEZONE).localize(tournament_datetime)
        
        # Check if it's at least 30 minutes in the future
        min_future_time = datetime.now(pytz.timezone(TIMEZONE)) + timedelta(minutes=30)
        
        return tournament_datetime > min_future_time
    except Exception as e:
        logger.error(f"Error validating tournament time: {e}")
        return False

def escape_markdown(text):
    """Escape markdown special characters"""
    if not text:
        return ""
    
    # Escape markdown special characters
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', str(text))

def truncate_text(text, max_length=100):
    """Truncate text with ellipsis"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."
