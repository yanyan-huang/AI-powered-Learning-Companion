from dotenv import load_dotenv
import os
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from openai import OpenAI
from moviepy.editor import AudioFileClip

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
    Processes user input and generates AI response within 150 words.
    Maintains conversation history for context.
    """
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=200,  # Approx. 150 words
        temperature=0.5,
        stop=["\n\n"]  # Encourages ChatGPT to end naturally at a logical stopping point
    )

    ai_reply = response.choices[0].message.content.strip()  # Extract AI response

    messages.append({"role": "assistant", "content": ai_reply})  # Store AI response for continuity
    return ai_reply

# =============================== #
#  Telegram Bot - Text Handling   #
# =============================== #

async def text_message(update: Update, context):
    """
    Handles incoming text messages, processes AI responses, and supports mode switching.
    """
    global current_mode

    user_input = update.message.text

    # Handle mode switching
    if user_input.lower().startswith("/mode"):
        mode_choice = user_input.split(" ", 1)[-1].strip().lower()
        if mode_choice in mode_prompts:
            current_mode = mode_choice
            messages.append({"role": "system", "content": mode_prompts[current_mode]})
            await update.message.reply_text(f"🔄 Mode switched to *{current_mode.capitalize()}*", parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("⚠️ Invalid mode. Choose from: mentor, tutor, interviewer.")
        return

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

# Start Bot using async polling
application.run_polling()