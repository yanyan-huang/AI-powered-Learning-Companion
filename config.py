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
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")  # Claude API ke

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")  # Telegram bot API token

# Raise errors if required keys are missing
if not AI_PROVIDER or AI_PROVIDER not in ("openai", "claude"):
    raise ValueError("⚠️ Invalid AI_PROVIDER. Must be 'openai' or 'claude'.")

if AI_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError("⚠️ Missing OPENAI_API_KEY in environment for OpenAI usage.")

if AI_PROVIDER == "claude" and not CLAUDE_API_KEY:
    raise ValueError("⚠️ Missing CLAUDE_API_KEY in environment for Claude usage.")

if not TELEGRAM_API_TOKEN:
    raise ValueError("⚠️ Missing TELEGRAM_API_TOKEN. The bot cannot run without it.")