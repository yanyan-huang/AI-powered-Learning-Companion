from dotenv import load_dotenv  # Load environment variables from a .env file
import os  # Access operating system environment variables

# ======================== #
#  Load API Keys & Config  #
# ======================== #

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API key
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")  # Telegram bot API token

# Raise an error if API keys are missing
if not OPENAI_API_KEY or not TELEGRAM_API_TOKEN:
    raise ValueError("⚠️ Missing API keys! Set OPENAI_API_KEY and TELEGRAM_API_TOKEN as environment variables.")