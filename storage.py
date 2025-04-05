import json
import os
from datetime import datetime

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
