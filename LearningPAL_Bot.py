from dotenv import load_dotenv  # Load environment variables from a .env file
import os  # Access operating system environment variables
from openai import OpenAI  # OpenAI API client for GPT-based interactions
from telegram import Update  # Handles updates (messages, commands) from Telegram users
from telegram.constants import ParseMode  # Constants for text formatting in Telegram messages
from telegram.ext import Application, CommandHandler, MessageHandler, filters  # Telegram bot framework for handling commands and messages
from moviepy.editor import AudioFileClip  # Handles audio file processing (converting voice messages)

# ======================== #
#  Load API Keys & Config  #
# ======================== #

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Raise error if API keys are missing
if not OPENAI_API_KEY or not TELEGRAM_API_TOKEN:
    raise ValueError("⚠️ Missing API keys! Set OPENAI_API_KEY and TELEGRAM_API_TOKEN as environment variables.")

# Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# ============================== #
#  AI Learning Modes for the Bot #
# ============================== #

mode_prompts = {
    "mentor": "You are an experienced Product Manager and mentor. Help guide aspiring product managers by designing their learning path, recommending resources (books, courses, tutorials), and offering career advice. Be encouraging.",
    "tutor": "You are an AI tutor for aspiring Product Managers. Provide detailed answers, simplify complex topics, and give real-world examples.",
    "interviewer": (
        "You are a Product Manager interview coach. Your process: "
        "1) Ask the user a behavioral or case-study question. "
        "2) Wait for their response. "
        "3) When the user finishes, assess all responses at once. "
        "4) Provide structured feedback on performance, strengths, weaknesses, and improvements."
    )
}

# Default mode (can be changed by user)
current_mode = "tutor"

# Store conversation history to maintain context
messages = [{"role": "system", "content": mode_prompts[current_mode]}]

# ======================== #
#  Chat Function with AI   #
# ======================== #

def chat_with_ai(user_input):
    """
    Processes user input and generates AI response based on the selected mode.
    Maintains conversation history for context.
    """
    messages.append({"role": "user", "content": user_input}) # Store user input for continuity
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    ai_reply = response.choices[0].message.content # Extract AI response
    messages.append({"role": "assistant", "content": ai_reply}) # Store AI response for continuity
    return ai_reply

# =============================== #
#  Telegram Bot - Text Handling   #
# =============================== #

async def change_mode(update: Update, context):
    """
    Handles /mode command to switch AI modes.
    """
    global current_mode

    # Check if user provided a mode argument
    if not context.args:
        await update.message.reply_text("⚠️ Please specify a mode. Example: /mode tutor")
        return

    mode_choice = context.args[0].lower()  # Extract mode from command arguments

    if mode_choice in mode_prompts:
        current_mode = mode_choice
        messages.clear()  # Reset conversation history when switching modes
        messages.append({"role": "system", "content": mode_prompts[current_mode]})
        await update.message.reply_text(f"🔄 Mode switched to *{current_mode.capitalize()}*", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("⚠️ Invalid mode. Choose from: mentor, tutor, interviewer.")

async def text_message(update: Update, context):
    """
    Handles incoming text messages, processes AI responses, and supports mode switching.
    """
    global current_mode

    user_input = update.message.text

    # Get AI Response
    ai_response = chat_with_ai(user_input)
    await update.message.reply_text(f"🤖 *LearningPal:* {ai_response}", parse_mode=ParseMode.MARKDOWN)

# =============================== #
#  Telegram Bot - Voice Handling  #
# =============================== #
async def voice_message(update: Update, context):
    """
    Handles voice messages: downloads, converts, transcribes, and processes them with AI.
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
        ).text  

    # Display transcribed text to the user
    await update.message.reply_text(f"🎙️ *You:* _{transcript}_", parse_mode=ParseMode.MARKDOWN)

    # Process the transcribed text as AI input
    ai_response = chat_with_ai(transcript)
    await update.message.reply_text(f"🤖 *LearningPal:* {ai_response}", parse_mode=ParseMode.MARKDOWN)

# ======================= #
#  Telegram Bot Setup     #
# ======================= #

# Initialize Telegram Bot application
application = Application.builder().token(TELEGRAM_API_TOKEN).build()

# Set Up Message Handlers
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
application.add_handler(MessageHandler(filters.VOICE, voice_message))

# Add a CommandHandler for /mode
application.add_handler(CommandHandler("mode", change_mode))

# Start Bot using async polling
application.run_polling()