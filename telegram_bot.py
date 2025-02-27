from telegram import Update  # Handles updates (messages, commands) from Telegram users
from telegram.constants import ParseMode  # Constants for text formatting in Telegram messages
from telegram.ext import Application, CommandHandler, MessageHandler, filters  # Telegram bot framework for handling commands and messages
from moviepy.editor import AudioFileClip  # Handles audio file processing (converting voice messages)
from config import TELEGRAM_API_TOKEN  # Load Telegram API token from config
from ai import chat_with_ai, switch_mode, client  # Import AI functions for chat and mode switching

# ======================== #
#  Initialize Telegram Bot #
# ======================== #

# Initialize Telegram Bot application
application = Application.builder().token(TELEGRAM_API_TOKEN).build()

# =============================== #
#  Command: Switch AI Learning Mode #
# =============================== #

async def change_mode(update: Update, context):
    """
    Handle /mode command to switch AI modes.
    """
    if not context.args:
        await update.message.reply_text("⚠️ Please specify a mode. Example: /mode tutor")
        return

    mode_choice = context.args[0].lower()  # Extract mode argument
    response_text = switch_mode(mode_choice)  # Call AI function to switch mode
    await update.message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)

# =============================== #
#  Message Handling - Text Input  #
# =============================== #

async def text_message(update: Update, context):
    """
    Handle incoming text messages and generate AI responses.
    """
    user_input = update.message.text  # Get user input

    ai_response = chat_with_ai(user_input)  # Get AI-generated response
    await update.message.reply_text(f"🤖 *LearningPal:* {ai_response}", parse_mode=ParseMode.MARKDOWN)

# =============================== #
#  Message Handling - Voice Input #
# =============================== #

async def voice_message(update: Update, context):
    """
    Handle voice messages: download, convert, transcribe, and process them with AI.
    """
    await update.message.reply_text("🎙️ Processing voice message...")

    # Download the voice message file from Telegram
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    await voice_file.download_to_drive("voice_message.ogg")

    # Convert .ogg to .mp3 using MoviePy
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")

    # Transcribe the audio using OpenAI Whisper model
    with open("voice_message.mp3", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        ).text  # Extract transcript text

    # Display transcribed text and process it with AI
    await update.message.reply_text(f"🎙️ *You:* _{transcript}_", parse_mode=ParseMode.MARKDOWN)
    ai_response = chat_with_ai(transcript)
    await update.message.reply_text(f"🤖 *LearningPal:* {ai_response}", parse_mode=ParseMode.MARKDOWN)

# ======================= #
#  Register Bot Handlers  #
# ======================= #

# Command Handler: Handles the "/mode" command to switch AI learning modes
application.add_handler(CommandHandler("mode", change_mode))

# Message Handler: Processes regular text messages (excluding commands) and generates AI responses
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))

# Message Handler: Processes voice messages, transcribes them, and sends them to AI
application.add_handler(MessageHandler(filters.VOICE, voice_message))

# ======================= #
#  Start Telegram Bot     #
# ======================= #

# Run the bot using polling
application.run_polling()