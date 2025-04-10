
from telegram.constants import ParseMode # Constants for text formatting in Telegram messages
from telegram import Update # Handles updates (messages, commands) from Telegram users
from moviepy.editor import AudioFileClip  # Handles audio file processing (converting voice messages)
from greetings import GREETINGS # Import greeting messages for different modes
from openai import OpenAI  # For Whisper speech-to-text
from config import OPENAI_API_KEY # Import OpenAI API key for Whisper

from llm_router import LLMRouter
from conversation_manager import ConversationManager
from bot_user import BotUser 

client = OpenAI(api_key=OPENAI_API_KEY) # Initialize OpenAI client for Whisper API

# ==================== #
#  Greeting Function   #
# ==================== #
async def greet_user(update):
    """
    Sends a warm and engaging welcome message when the user first interacts with the bot.
    """
    await update.message.reply_text(
        "👋 Hi! I'm *PM Pal*, your dedicated * AI mentor, coach, and mock interviewer* on your Product Management journey!🚀\n\n"
        "Think of me as your *always-there learning companion*—whether you're exploring PM fundamentals, refining your skills, or prepping for high-stakes interviews, I’ve got your back. \n\n",
        parse_mode="Markdown"
    )

# ======================================= #
# Helper Function: Ensure Mode Selected #
# ======================================= #
async def ensure_mode_selected(update, user):
    """
    Checks if the user has selected a mode. 
    If not, sends a reminder and stops further execution.
    Returns True if mode is missing, otherwise False.
    """
    if not user.mode:
        await update.message.reply_text(
            "🎯 **Ready to dive in? Choose a mode to tailor your learning experience today!**\n\n"
            " **💡`/mode mentor`** for career advice & learning paths.\n"
            " **📘`/mode coach`** to learn PM concepts & case studies interactively.\n"
            " **🎤`/mode interviewer`** to practice PM interviews and get feedback.\n\n"
            "Let me know how you'd like to begin!",
            parse_mode="Markdown"
        )
        return True  # Indicates that the mode is missing
    return False  # Mode is set, continue processing

# =============================== #
#  Command Handling - Start       #
# =============================== # 
async def start(update, context):
    """
    Handles the /start command: greets the user and resets their mode.
    """
    user_id = update.message.chat_id
    user = BotUser(user_id)
    user.mode = None
    await greet_user(update)
    await ensure_mode_selected(update, user)

# =============================== #
#  Command Handling - Help         #
# =============================== #
async def help_command(update: Update, context):
    """
    Provides users with a quick overview of available commands and bot functionality.
    """
    await update.message.reply_text(
        "**🤖 Need Help for your PM journey? Here's What You Can Do:**\n\n"
        "- **💡 Type** `/mode mentor` for career guidance and learning paths.\n"
        "- **📘 Type** `/mode coach` to learn PM concepts & case studies interactively.\n"
        "- **🎤 Type** `/mode interviewer` for mock interviews with feedback.\n\n"
        "**Other Commands:**\n"
        "- **/start** – Restart the bot and reset your session.\n"
        "- **/help** – Show this help message anytime.\n\n"
        "Once you've selected a mode, just ask me anything, and I'll guide you!",
        parse_mode="Markdown"
    )

# ================================== #
#  Command Handling - Mode Switching #
# ================================== #

async def change_mode(update: Update, context):
    """
    Handle /mode command and update mode for the specific user.
    """
    user_id = update.message.chat_id
    user = BotUser(user_id)
    router = LLMRouter()
    manager = ConversationManager(user, router)

    #  validate user input for mode change 
    if not context.args:
        await update.message.reply_text("Please choose `/mode mentor`, `/mode coach`, or `/mode interviewer`.")
        return

    mode_choice = context.args[0].lower()
    valid_modes = ["mentor", "coach", "interviewer"]

    if mode_choice not in valid_modes:
        await update.message.reply_text("Please choose `/mode mentor`, `/mode coach`, or `/mode interviewer`.")
        return

    #  Switch mode and update user data
    result = manager.switch_mode(mode_choice)
    await update.message.reply_text(
        f"💡 *Mode switched to {mode_choice.capitalize()} Mode.*\n\n{GREETINGS[mode_choice]}",
        parse_mode=ParseMode.MARKDOWN
    )


# =============================== #
#  Message Handling - Text Input  #
# =============================== #

async def text_message(update: Update, context):
    """
    Handle incoming text messages and generate AI responses.
    If no mode is selected, reminds the user to choose one.
    """
    user_id = update.message.chat_id
    user_input = update.message.text.strip().lower()
    user = BotUser(user_id)

    # Use helper function to ensure user selects a mode first
    if await ensure_mode_selected(update, user):
        return  # Exit early if mode is missing

    router = LLMRouter()
    manager = ConversationManager(user, router)
    ai_response = manager.process_input(user_input)

    await update.message.reply_text(
        f"🤖 *PM Pal:* {ai_response}"
        # parse_mode=ParseMode.MARKDOWN
    )

# =============================== #
#  Message Handling - Voice Input #
# =============================== #

async def voice_message(update: Update, context):
    """
    Handle voice messages: download, convert, transcribe, and process them with AI.
    """
    user_id = update.message.chat_id
    user = BotUser(user_id)

    # Use helper function to ensure user selects a mode first
    if await ensure_mode_selected(update, user):
        return  # Exit early if mode is missing

    await update.message.reply_text("🎙️ Processing voice message...")

    # Process Voice Message
    # Download the voice message file from Telegram
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    await voice_file.download_to_drive("voice_message.ogg")

    # Convert .ogg to .mp3 using MoviePy
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")

    # Transcribe the audio using Whisper
    try:
        with open("voice_message.mp3", "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            ).text
    except Exception as e:
        await update.message.reply_text(f"❌ Error transcribing audio: {e}")
        return

    # Display transcribed text and process it with AI
    await update.message.reply_text(
        f"🎙️ *You:* _{transcript}_" 
        # parse_mode=ParseMode.MARKDOWN
        )

    # Generate AI response
    router = LLMRouter()
    manager = ConversationManager(user, router)
    ai_response = manager.process_input(transcript, source="voice")
    await update.message.reply_text(
        f"🤖 *PM Pal:* {ai_response}" 
        # parse_mode=ParseMode.MARKDOWN
        )