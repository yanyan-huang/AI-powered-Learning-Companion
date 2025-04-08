from config import TELEGRAM_API_TOKEN  # Load Telegram API token from config
from telegram.ext import Application, CommandHandler, MessageHandler, filters  # Telegram bot framework for handling commands and messages
from handlers import text_message, change_mode, voice_message  # Import all handlers
from handlers import start, help_command  # Import new start function

# ======================== #
#  Initialize Telegram Bot #
# ======================== #

# Initialize Telegram Bot application
application = Application.builder().token(TELEGRAM_API_TOKEN).build()

# ======================= #
#  Register Bot Handlers  #
# ======================= #

# Command Handler: Handles the "/start" command to greet the user and reset their mode
application.add_handler(CommandHandler("start", start))

# Command Handler: Handles the "/mode" command to switch AI learning modes
application.add_handler(CommandHandler("mode", change_mode))

# Command Handler: Handles the "/help" command to provide guidance on using the bot
application.add_handler(CommandHandler("help", help_command))

# Message Handler: Processes regular text messages (excluding commands) and generates AI responses
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))

# Message Handler: Processes voice messages, transcribes them, and sends them to AI
application.add_handler(MessageHandler(filters.VOICE, voice_message))

# ======================= #
#  Start Telegram Bot     #
# ======================= #

# Run the bot using polling
application.run_polling()