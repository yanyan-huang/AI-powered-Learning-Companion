from dotenv import load_dotenv  # Load environment variables from a .env file
import os  # Access operating system environment variables

# ======================== #
#  Load API Keys & Config  #
# ======================== #

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # AI provider (default: OpenAI)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API key
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")  # Claude API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Load Gemini API key
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4") # Default model to use

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")  # Telegram bot API token

# Raise errors if required keys are missing
if AI_PROVIDER not in ["openai", "claude", "gemini"]:
    raise ValueError("⚠️ Invalid AI_PROVIDER. Must be 'openai', 'claude', or 'gemini'.")

if AI_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError("⚠️ Missing OPENAI_API_KEY in environment for OpenAI usage.")

if AI_PROVIDER == "claude" and not CLAUDE_API_KEY:
    raise ValueError("⚠️ Missing CLAUDE_API_KEY in environment for Claude usage.")

if AI_PROVIDER == "gemini" and not GOOGLE_API_KEY:
    raise ValueError("⚠️ Missing GOOGLE_API_KEY in environment for Gemini usage.")

if not TELEGRAM_API_TOKEN:
    raise ValueError("⚠️ Missing TELEGRAM_API_TOKEN. The bot cannot run without it.")

# Available LLMs and models
AVAILABLE_MODELS = {
    "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
    "claude": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"],
    "gemini": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-pro-vision"]
}

# Default model to use if user has not selected any
DEFAULT_MODEL = {
    "openai": "gpt-4",
    "claude": "claude-3-sonnet-20240229",
    "gemini": "gemini-1.5-pro"
}