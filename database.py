"""
Database operations for the BGMI Tournament Bot
"""

import pymongo
from datetime import datetime, timedelta
import pytz
from config import MONGODB_URI, DATABASE_NAME, TIMEZONE
import logging

logger = logging.getLogger(__name__)

# Global database connection
client = None
db = None

def init_database():
    """Initialize database connection"""
    global client, db
    try:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client[DATABASE_NAME]
        
        # Create indexes
        db.users.create_index("user_id", unique=True)
        db.tournaments.create_index("tournament_id", unique=True)
        db.payments.create_index([("user_id", 1), ("tournament_id", 1)])
        
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

def get_user(user_id):
    """Get user by ID"""
    try:
        return db.users.find_one({"user_id": user_id})
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return None

def create_user(user_data):
    """Create new user"""
    try:
        user_data["joined_at"] = datetime.now(pytz.timezone(TIMEZONE))
        user_data["balance"] = 0
        user_data["total_tournaments"] = 0
        user_data["total_wins"] = 0
        user_data["is_banned"] = False
        result = db.users.insert_one(user_data)
        return result.inserted_id
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return None

def update_user(user_id, update_data):
    """Update user data"""
    try:
        result = db.users.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        return False

def generate_referral_code(user_id):
    """Generate unique referral code"""
    import random
    import string
    
    while True:
        code = "REF" + ''.join(random.choices(string.digits, k=6))
        existing = db.users.find_one({"referral_code": code})
        if not existing:
            return code

def create_tournament(tournament_data):
    """Create new tournament"""
    try:
        tournament_data["created_at"] = datetime.now(pytz.timezone(TIMEZONE))
        tournament_data["participants"] = []
        tournament_data["status"] = "upcoming"
        tournament_data["room_shared"] = False
        result = db.tournaments.insert_one(tournament_data)
        return result.inserted_id
    except Exception as e:
        logger.error(f"Error creating tournament: {e}")
        return None

def get_tournament(tournament_id):
    """Get tournament by ID"""
    try:
        return db.tournaments.find_one({"tournament_id": tournament_id})
    except Exception as e:
        logger.error(f"Error getting tournament {tournament_id}: {e}")
        return None

def get_active_tournaments():
    """Get all active tournaments"""
    try:
        return list(db.tournaments.find({"status": {"$in": ["upcoming", "active"]}}))
    except Exception as e:
        logger.error(f"Error getting active tournaments: {e}")
        return []

def join_tournament(user_id, tournament_id):
    """Add user to tournament"""
    try:
        result = db.tournaments.update_one(
            {"tournament_id": tournament_id},
            {"$addToSet": {"participants": user_id}}
        )
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error joining tournament: {e}")
        return False

def create_payment_request(user_id, tournament_id, amount, utr_number=None):
    """Create payment request"""
    try:
        payment_data = {
            "user_id": user_id,
            "tournament_id": tournament_id,
            "amount": amount,
            "utr_number": utr_number,
            "status": "pending",
            "created_at": datetime.now(pytz.timezone(TIMEZONE)),
            "confirmed_at": None,
            "confirmed_by": None
        }
        result = db.payments.insert_one(payment_data)
        return result.inserted_id
    except Exception as e:
        logger.error(f"Error creating payment request: {e}")
        return None

def confirm_payment(user_id, tournament_id, admin_id):
    """Confirm payment"""
    try:
        result = db.payments.update_one(
            {"user_id": user_id, "tournament_id": tournament_id},
            {
                "$set": {
                    "status": "confirmed",
                    "confirmed_at": datetime.now(pytz.timezone(TIMEZONE)),
                    "confirmed_by": admin_id
                }
            }
        )
        
        if result.modified_count > 0:
            # Update user's paid status for the tournament
            db.users.update_one(
                {"user_id": user_id},
                {"$set": {"paid": True, "confirmed": True}}
            )
        
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error confirming payment: {e}")
        return False

def decline_payment(user_id, tournament_id, admin_id):
    """Decline payment"""
    try:
        result = db.payments.update_one(
            {"user_id": user_id, "tournament_id": tournament_id},
            {
                "$set": {
                    "status": "declined",
                    "declined_at": datetime.now(pytz.timezone(TIMEZONE)),
                    "declined_by": admin_id
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error declining payment: {e}")
        return False

def get_financial_data(period="today"):
    """Get financial data for specified period"""
    try:
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)
        
        if period == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        else:
            start_date = datetime.min.replace(tzinfo=tz)
        
        pipeline = [
            {
                "$match": {
                    "status": "confirmed",
                    "confirmed_at": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_amount": {"$sum": "$amount"},
                    "total_payments": {"$sum": 1}
                }
            }
        ]
        
        result = list(db.payments.aggregate(pipeline))
        if result:
            return result[0]
        return {"total_amount": 0, "total_payments": 0}
    except Exception as e:
        logger.error(f"Error getting financial data: {e}")
        return {"total_amount": 0, "total_payments": 0}

def ban_user(user_id, admin_id, reason=""):
    """Ban user"""
    try:
        result = db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_banned": True,
                    "banned_at": datetime.now(pytz.timezone(TIMEZONE)),
                    "banned_by": admin_id,
                    "ban_reason": reason
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error banning user {user_id}: {e}")
        return False

def unban_user(user_id, admin_id):
    """Unban user"""
    try:
        result = db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_banned": False,
                    "unbanned_at": datetime.now(pytz.timezone(TIMEZONE)),
                    "unbanned_by": admin_id
                },
                "$unset": {
                    "banned_at": "",
                    "banned_by": "",
                    "ban_reason": ""
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error unbanning user {user_id}: {e}")
        return False

def is_user_banned(user_id):
    """Check if user is banned"""
    try:
        user = db.users.find_one({"user_id": user_id})
        return user and user.get("is_banned", False)
    except Exception as e:
        logger.error(f"Error checking ban status for user {user_id}: {e}")
        return False

def get_user_match_history(user_id):
    """Get user's match history"""
    try:
        tournaments = list(db.tournaments.find(
            {"participants": user_id},
            {"name": 1, "date": 1, "type": 1, "status": 1}
        ).sort("created_at", -1).limit(10))
        return tournaments
    except Exception as e:
        logger.error(f"Error getting match history for user {user_id}: {e}")
        return []

def update_tournament_status(tournament_id, status):
    """Update tournament status"""
    try:
        result = db.tournaments.update_one(
            {"tournament_id": tournament_id},
            {"$set": {"status": status}}
        )
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error updating tournament status: {e}")
        return False

def delete_tournament(tournament_id):
    """Delete tournament"""
    try:
        result = db.tournaments.delete_one({"tournament_id": tournament_id})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error deleting tournament: {e}")
        return False
