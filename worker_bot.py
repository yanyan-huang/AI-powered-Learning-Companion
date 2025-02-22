import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Bot
from moviepy.editor import AudioFileClip

"""Processes Messages from Queue & Sends AI Responses"""

# Load environment variables
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_API_TOKEN)

# Simple in-memory queue
message_queue = asyncio.Queue()

# ======================== #
#  Chat Function with AI   #
# ======================== #
messages = [{"role": "system", "content": "You are an AI tutor."}]

def chat_with_ai(user_input):
    """Processes user input and generates AI response while maintaining context"""
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=200  # Limit the response length
    )
    ai_reply = response.choices[0].message.content  # Extract AI response
    messages.append({"role": "assistant", "content": ai_reply})
    
    return ai_reply

# ======================== #
#  Worker Process          #
# ======================== #
async def worker():
    """Continuously fetches and processes messages from the queue"""
    while True:
        msg_type, user_id, content = await message_queue.get()

        if msg_type == "text":
            ai_reply = chat_with_ai(content)
            await bot.send_message(chat_id=user_id, text=f"🤖 *LearningPal:* {ai_reply}", parse_mode="Markdown")

        elif msg_type == "voice":
            # Convert voice to MP3
            audio_clip = AudioFileClip(content)
            mp3_path = content.replace(".ogg", ".mp3")
            audio_clip.write_audiofile(mp3_path)

            # Transcribe the voice message
            with open(mp3_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file).text

            await bot.send_message(chat_id=user_id, text=f"🎙️ *You:* _{transcript}_", parse_mode="Markdown")

            # Process the transcribed text with AI
            ai_reply = chat_with_ai(transcript)
            await bot.send_message(chat_id=user_id, text=f"🤖 *LearningPal:* {ai_reply}", parse_mode="Markdown")

        message_queue.task_done()

async def start_worker():
    asyncio.create_task(worker())

if __name__ == "__main__":
    asyncio.run(start_worker())