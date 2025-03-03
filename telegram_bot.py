from config import TELEGRAM_API_TOKEN  # Load Telegram API token from config
from telegram import Update  # Handles updates (messages, commands) from Telegram users
from telegram.constants import ParseMode  # Constants for text formatting in Telegram messages
from telegram.ext import Application, CommandHandler, MessageHandler, filters  # Telegram bot framework for handling commands and messages
from handlers import text_message, change_mode, voice_message  # Import all handlers
from handlers import greet_user, ensure_mode_selected, start  # Import new start function

# ======================== #
#  Initialize Telegram Bot #
# ======================== #

# Initialize Telegram Bot application
application = Application.builder().token(TELEGRAM_API_TOKEN).build()

# Track user states and selected modes per user
user_states = {}  # Stores whether a user has been greeted
user_modes = {}   # Stores selected mode per user (no default mode)

# ======================= #
#  Register Bot Handlers  #
# ======================= #

# Command Handler: Handles the "/start" command to greet the user and reset their mode
application.add_handler(CommandHandler("start", lambda update, context: start(update, context, user_modes)))

# Command Handler: Handles the "/mode" command to switch AI learning modes
application.add_handler(CommandHandler("mode", lambda update, context: change_mode(update, context, user_modes)))

# Message Handler: Processes regular text messages (excluding commands) and generates AI responses
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: text_message(update, context, user_modes)))

# Message Handler: Processes voice messages, transcribes them, and sends them to AI
application.add_handler(MessageHandler(filters.VOICE, lambda update, context: voice_message(update, context, user_modes)))

# ======================= #
#  Start Telegram Bot     #
# ======================= #

# Run the bot using polling
application.run_polling()