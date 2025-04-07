import json
import os
from datetime import datetime

from config import DEFAULT_MODEL, AI_PROVIDER, AVAILABLE_MODELS

# ================================ #
#  Directory for Saving User Data  #
# ================================ #

USER_DATA_DIR = "user_data"

# Ensure the directory exists
os.makedirs(USER_DATA_DIR, exist_ok=True)

# ================================ #
#  Load User Data from JSON File   #
# ================================ #

def load_user_data(user_id):
    """
    Load user data from their local JSON file.

    Args:
        user_id (int or str): Unique Telegram user ID

    Returns:
        dict: User data with keys like "mode", "history", etc.
    """
    filepath = os.path.join(USER_DATA_DIR, f"{user_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    else:
        return {"mode": None, "history": []}  # Default empty structure

# ================================ #
#  Save User Data to JSON File     #
# ================================ #

def save_user_data(user_id, data):
    """
    Persist user data to local JSON file.

    Args:
        user_id (int or str): Unique Telegram user ID
        data (dict): The user data to save
    """
    filepath = os.path.join(USER_DATA_DIR, f"{user_id}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

# ================================ #
#  Update Selected User Mode       #
# ================================ #

def set_mode(user_id, mode):
    """
    Store the current selected mode ("mentor", "coach", "interviewer").

    Args:
        mode (str): The active mode chosen by user
    """
    data = load_user_data(user_id)
    data["mode"] = mode
    save_user_data(user_id, data)

# ================================ #
#  Add Interaction to Chat History #
# ================================ #

def add_to_history(user_id, message, role="user", source=None, mode=None):
    """
    Add a message to the user's conversation history with optional metadata.

    Args:
        user_id: Telegram user ID
        message: The message content
        role: "user" or "assistant"
        source: "text", "transcript", etc.
        mode: "mentor", "coach", or "interviewer"
    """
    data = load_user_data(user_id)

    entry = {
        "role": role,
        "content": message,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Add metadata
    if source:
        entry["source"] = source
    if mode:
        entry["mode"] = mode

    data["history"].append(entry)
    save_user_data(user_id, data)

# ================================ #
#  Log Full User/AI Interaction    #
# ================================ #

def log_interaction(user_id, user_input, ai_response, input_source="text", mode=None):
    """
    Log user input and AI reply with role, mode, and input source.

    Args:
        user_id: Telegram user ID
        user_input: User's input message
        ai_response: AI's generated response
        input_source: Source of the input (e.g., "text", "voice")
        mode: Current mode ("mentor", "coach", "interviewer")
    """
    add_to_history(user_id, user_input, role="user", source=input_source, mode=mode)
    add_to_history(user_id, ai_response, role="assistant", source="text", mode=mode)

# ================================ #
#  Load and Save Model Selection   #
# ================================ #
def set_user_model(user_id, provider, model_name):
    """
    Save the selected model under the specified provider for the user.

    Args:
        user_id: Telegram user ID
        provider: LLM provider (e.g., "openai")
        model_name: Model name (e.g., "gpt-4")
    """
    if provider not in AVAILABLE_MODELS:
        raise ValueError(f"⚠️ Unsupported provider: {provider}")
    if model_name not in AVAILABLE_MODELS[provider]:
        raise ValueError(f"⚠️ Invalid model '{model_name}' for provider '{provider}'.")

    data = load_user_data(user_id)
    data["model"] = {
        "provider": provider,
        "model_name": model_name
    }
    save_user_data(user_id, data)

def get_user_model(user_id, provider):
    """
    Retrieve the selected model for a specific provider for a user.
    Falls back to default model if not set.
    Args:
        user_id: Telegram user ID
        provider: AI provider (e.g., "openai", "claude", "gemini")
    Returns:
        str: The model name selected by the user or the default model
    """
    
    data = load_user_data(user_id)
    user_models = data.get("model", {})
    return user_models.get(provider, AVAILABLE_MODELS[provider][0])  # Default to first model

def get_active_provider(user_id):
    """
    Retrieve the active AI provider for a user.
    Args:
        user_id: Telegram user ID
    Returns:
        str: The AI provider selected by the user or the default provider
    """
    data = load_user_data(user_id)
    model_info = data.get("model", {})
    return model_info.get("provider", AI_PROVIDER)

