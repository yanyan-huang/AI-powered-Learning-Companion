import asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters

print("Starting webhook server on port 8443...")  # Before running the webhook
"""Handles Incoming Messages & Queues Processing"""

# Load environment variables
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Simple in-memory queue (For now, replace with Redis later)
message_queue = asyncio.Queue()

# Initialize Telegram Bot
application = Application.builder().token(TELEGRAM_API_TOKEN).build()

async def text_message(update: Update, context):
    print(f"📩 Received message from {update.message.chat_id}: {update.message.text}")
    """Handles incoming text messages and queues them for processing"""
    user_input = update.message.text
    user_id = update.message.chat_id

    # Add message to the processing queue
    await message_queue.put(("text", user_id, user_input))
    
    await update.message.reply_text("📩 Your message is being processed...")

async def voice_message(update: Update, context):
    """Handles voice messages, downloads them, and queues them for transcription"""
    await update.message.reply_text("🎙️ Processing voice message...")

    voice_file = await context.bot.get_file(update.message.voice.file_id)
    file_path = f"voice_message_{update.message.chat_id}.ogg"
    await voice_file.download_to_drive(file_path)

    await message_queue.put(("voice", update.message.chat_id, file_path))
    
    await update.message.reply_text("🎙️ Voice received! Processing transcription...")

# Set Up Message Handlers
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
application.add_handler(MessageHandler(filters.VOICE, voice_message))

# Start the bot using Webhook
WEBHOOK_URL = "https://ai-powered-learning-companion-ryvl.onrender.com"
application.run_webhook(
    listen="0.0.0.0",
    port=int(os.getenv("PORT", 8443)),
    url_path=os.getenv("TELEGRAM_API_TOKEN"),
    webhook_url=f"{WEBHOOK_URL}/{os.getenv('TELEGRAM_API_TOKEN')}"
)