#!/usr/bin/env python3
"""
BGMI Tournament Management Telegram Bot
🚫 No Mercy 🚫
"""


import handlers.user_handlers as user_handlers
import os
sys.path.append(os.path.dirname(__file__))
import os
print("Current working directory:", os.getcwd())
print("Files in current dir:", os.listdir())
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime
import pytz
from config import *
from database import init_database
from handlers.user_handlers import (
    start, check_membership, show_menu, invite_friends, match_history, help_command,
    show_active_tournaments, show_terms_conditions, share_whatsapp_status
)
from handlers.admin_handlers import (
    admin_panel, host_tournament, ai_host, active_tournaments, drop_room, 
    list_players, clear_tournament, data_vault, special_notification, 
    ban_user_handler, unban_user_handler, confirm_payment_handler, decline_payment_handler
)
from handlers.payment_handlers import paid_command, process_utr
from handlers.tournament_handlers import join_tournament, tournament_rules, tournament_disclaimer

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Initialize database
    init_database()
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # User handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_membership, pattern="^check_membership$"))
    application.add_handler(CallbackQueryHandler(show_menu, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(invite_friends, pattern="^invite_friends$"))
    application.add_handler(CallbackQueryHandler(show_active_tournaments, pattern="^active_tournaments$"))
    application.add_handler(CallbackQueryHandler(show_terms_conditions, pattern="^terms_conditions$"))
    application.add_handler(CallbackQueryHandler(share_whatsapp_status, pattern="^share_whatsapp$"))
    application.add_handler(CallbackQueryHandler(match_history, pattern="^match_history$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^help$"))
    application.add_handler(CommandHandler("matchhistory", match_history))
    application.add_handler(CommandHandler("help", help_command))
    
    # Tournament handlers
    application.add_handler(CallbackQueryHandler(join_tournament, pattern="^join_tournament_"))
    application.add_handler(CallbackQueryHandler(tournament_rules, pattern="^tournament_rules_"))
    application.add_handler(CallbackQueryHandler(tournament_disclaimer, pattern="^tournament_disclaimer_"))
    
    # Payment handlers
    application.add_handler(CommandHandler("paid", paid_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_utr))
    
    # Admin handlers
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("host", host_tournament))
    application.add_handler(CommandHandler("aihost", ai_host))
    application.add_handler(CommandHandler("active", active_tournaments))
    application.add_handler(CommandHandler("droproom", drop_room))
    application.add_handler(CommandHandler("listplayers", list_players))
    application.add_handler(CommandHandler("clear", clear_tournament))
    application.add_handler(CommandHandler("datavault", data_vault))
    application.add_handler(CommandHandler("special", special_notification))
    application.add_handler(CommandHandler("ban", ban_user_handler))
    application.add_handler(CommandHandler("unban", unban_user_handler))
    application.add_handler(CommandHandler("confirm", confirm_payment_handler))
    application.add_handler(CommandHandler("decline", decline_payment_handler))
    
    # Tournament creation callbacks
    application.add_handler(CallbackQueryHandler(host_tournament, pattern="^host_"))
    application.add_handler(CallbackQueryHandler(ai_host, pattern="^aihost_"))
    
    # Start the bot
    logger.info("🚫 No Mercy Bot is starting...")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == '__main__':
    main()
