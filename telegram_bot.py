from config import TELEGRAM_API_TOKEN  # Load Telegram API token from config
from telegram.ext import Application, CommandHandler, MessageHandler, filters  # Telegram bot framework for handling commands and messages
from handlers import text_message, change_mode, voice_message  # Import all handlers
from handlers import start, help_command  # Import new start function
from handlers import mode_mentor, mode_coach, mode_interview  # Import specific mode handlers
from config import USE_WEBHOOK, WEBHOOK_URL, PORT  # Import webhook settings

### DEBUGGING ###
import traceback
import os
print("🟢 Starting PM Pal container...", flush=True)
print("📦 PORT =", os.getenv("PORT"), flush=True)
print("📦 WEBHOOK_URL =", os.getenv("WEBHOOK_URL"), flush=True)
print("📦 TELEGRAM_API_TOKEN =", os.getenv("TELEGRAM_API_TOKEN"), flush=True)
print("📦 FIREBASE_CRED_PATH =", os.getenv("FIREBASE_CRED_PATH"), flush=True)
print("📦 USE_WEBHOOK =", os.getenv("USE_WEBHOOK"), flush=True)

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

# Command Handler: Handles the "/mentor", "/coach", and "/interview" commands to set the respective modes
application.add_handler(CommandHandler("mentor", mode_mentor))  # Direct /mentor
application.add_handler(CommandHandler("coach", mode_coach))    # Direct /coach
application.add_handler(CommandHandler("interviewer", mode_interview))  # Direct /interview

# Command Handler: Handles the "/help" command to provide guidance on using the bot
application.add_handler(CommandHandler("help", help_command))

# Message Handler: Processes regular text messages (excluding commands) and generates AI responses
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))

# Message Handler: Processes voice messages, transcribes them, and sends them to AI
application.add_handler(MessageHandler(filters.VOICE, voice_message))

# ======================= #
#  Start Telegram Bot     #
# ======================= #

# import threading
# from flask import Flask

# flask_app = Flask(__name__)

# @flask_app.route("/")
# def health_check():
#     return "PM Pal is alive!", 200

# def run_flask():
#     flask_app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    try:
        if USE_WEBHOOK and WEBHOOK_URL:
            print("🌐 PM Pal running in webhook mode", flush=True)

            # # Start Flask in a background thread
            # threading.Thread(target=run_flask).start()

            # Start Telegram bot with webhook
            application.run_webhook(
                listen="0.0.0.0",
                port=PORT,
                url_path=TELEGRAM_API_TOKEN,
                webhook_url=WEBHOOK_URL
            )
        else:
            print("🤖 PM Pal running in polling mode", flush=True)
            application.run_polling()

    except Exception as e:
        print("❌ ERROR during startup:", flush=True)
        traceback.print_exc()