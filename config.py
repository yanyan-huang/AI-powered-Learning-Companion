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

# List of whitelisted user IDs (comma-separated)
WHITELISTED_USER_IDS = os.getenv("WHITELISTED_USER_IDS", "").split(",")  

# polling or webhook for Telegram bot  ：Set to True for webhook, False for polling
# Webhook is more efficient, but requires a public URL; Polling is easier to set up, but less efficient
USE_WEBHOOK = os.getenv("USE_WEBHOOK", "false").lower() == "true"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8080))  # Default to 8080 (used by Cloud Run)