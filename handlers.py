from ai import chat_with_ai, client  # Import AI functions for chat and mode switching
from telegram.constants import ParseMode # Constants for text formatting in Telegram messages
from telegram import Update # Handles updates (messages, commands) from Telegram users
from moviepy.editor import AudioFileClip  # Handles audio file processing (converting voice messages)

# =============================== #
#  Greeting Function              #
# =============================== #
async def greet_user(update):
    """
    Sends a warm and engaging welcome message when the user first interacts with the bot.
    """
    await update.message.reply_text(
        "👋 Hi! I'm your AI *Learning Pal*, your dedicated *mentor, tutor, and mock interviewer* on your Product Management journey!🚀\n\n"
        "Think of me as your *always-there learning companion*—whether you're exploring PM fundamentals, refining your skills, or prepping for high-stakes interviews, I’ve got your back. \n\n",
        parse_mode="Markdown"
    )

# ======================================= #
# Helper Function: Ensure Mode Selected #
# ======================================= #
async def ensure_mode_selected(update, user_modes):
    """
    Checks if the user has selected a mode. 
    If not, sends a reminder and stops further execution.
    Returns True if mode is missing, otherwise False.
    """
    user_id = update.message.chat_id

    if user_modes.get(user_id) is None:
        await update.message.reply_text(
            "🎯 **Ready to dive in? Choose a mode to tailor your learning experience today!**\n\n"
            "- **`/mode mentor`** to gain career insights, industry advice, and strategic learning paths.\n"
            "- **`/mode tutor`** to engage in interactive Q&A to master core PM concepts.\n"
            "- **`/mode interviewer`** to practice PM interviews and receive feedback.\n\n"
            "Let me know how you'd like to begin!",
            parse_mode="Markdown"
        )
        return True  # Indicates that the mode is missing

    return False  # Mode is set, continue processing

# =============================== #
#  Command Handling - Start       #
# =============================== # 
async def start(update, context, user_modes):
    """
    Handles the /start command: greets the user and resets their mode.
    """
    user_id = update.message.chat_id
    user_modes[user_id] = None  # Reset mode on /start

    await greet_user(update)  # Call the greeting function
    await ensure_mode_selected(update, user_modes)  # Ask user to select a mode


# ================================== #
#  Command Handling - Mode Switching #
# ================================== #

async def change_mode(update: Update, context, user_modes):
    """
    Handle /mode command and update mode for the specific user.
    """
    user_id = update.message.chat_id

    #  validate user input for mode change 
    if not context.args:
        await update.message.reply_text("Please choose `/mode mentor`, `/mode tutor`, or `/mode interviewer`.")
        return

    mode_choice = context.args[0].lower()
    valid_modes = ["mentor", "tutor", "interviewer"]

    if mode_choice not in valid_modes:
        await update.message.reply_text("Please choose `/mode mentor`, `/mode tutor`, or `/mode interviewer`.")
        return

    # store selected mode for the user
    user_modes[user_id] = mode_choice
    await update.message.reply_text(f"💡*Mode switched to {mode_choice.capitalize()} Mode.* You can now ask related questions!", parse_mode=ParseMode.MARKDOWN)

# =============================== #
#  Message Handling - Text Input  #
# =============================== #

async def text_message(update: Update, context, user_modes):
    """
    Handle incoming text messages and generate AI responses.
    If no mode is selected, reminds the user to choose one.
    """
    user_id = update.message.chat_id
    user_input = update.message.text.strip().lower()

    # Use helper function to ensure user selects a mode first
    if await ensure_mode_selected(update, user_modes):
        return  # Exit early if mode is missing

    #  Generate AI Response Based on Mode #
    ai_response = chat_with_ai(user_id, user_input, user_modes[user_id])
    await update.message.reply_text(f"🤖 *LearningPal:* {ai_response}", parse_mode="Markdown")

# =============================== #
#  Message Handling - Voice Input #
# =============================== #

async def voice_message(update: Update, context, user_modes):
    """
    Handle voice messages: download, convert, transcribe, and process them with AI.
    """
    user_id = update.message.chat_id

    # Use helper function to ensure user selects a mode first
    if await ensure_mode_selected(update, user_modes):
        return  # Exit early if mode is missing

    await update.message.reply_text("🎙️ Processing voice message...")

    # Process Voice Message
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

    # Generate AI response
    ai_response = chat_with_ai(user_id, transcript, user_modes[user_id])
    await update.message.reply_text(f"🤖 *LearningPal:* {ai_response}", parse_mode=ParseMode.MARKDOWN)