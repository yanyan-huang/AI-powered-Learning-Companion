# This is used to save conversation mode, history, transcripts, etc.
# Currently stores data as local JSON files per user
# -----------------------------------------

import os
import json
from datetime import datetime # for timestamps

# Base directory where all user JSON files are stored
STORAGE_DIR = "user_data"

# Make sure the directory exists at runtime
os.makedirs(STORAGE_DIR, exist_ok=True)

# ============================== #
#    Internal Helper Function    #
# ============================== #

def _get_path(user_id):
    """
    Get the full file path for a user's JSON file.

    Args:
        user_id (int or str): Unique Telegram user ID.
    
    Returns:
        str: Path to JSON file for that user.
    """
    return os.path.join(STORAGE_DIR, f"{user_id}.json")

# ============================== #
#   Load & Save Entire Session   #
# ============================== #

def load_user_data(user_id):
    """
    Load existing user data from disk, or return a default structure.

    Returns:
        dict: user session data containing:
            - mode (str): active learning mode
            - history (list): past text inputs
            - transcripts (list): past voice-to-text entries
    """
    path = _get_path(user_id)

    # Return stored data if it exists
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)

    # Default template for a new user
    return {
        "mode": None,
        "history": [],
        "transcripts": []
    }

def save_user_data(user_id, data):
    """
    Save updated user data to disk (overwrite).

    Args:
        user_id: Telegram user ID
        data (dict): full session data
    """
    path = _get_path(user_id)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ============================== #
#     Update Individual Fields   #
# ============================== #

def set_mode(user_id, mode):
    """
    Update the user's current learning mode and persist.

    Args:
        mode (str): 'mentor', 'coach', or 'interviewer'
    """
    data = load_user_data(user_id)
    data["mode"] = mode
    save_user_data(user_id, data)

def add_to_history(user_id, message, role="user"):
    """
    Add a message to the user's history log with role and timestamp.

    Args:
        message (str): Message content
        role (str): "user" or "assistant"
    """
    data = load_user_data(user_id)
    data["history"].append({
        "role": role,
        "content": message,
        "timestamp": datetime.utcnow().isoformat()
    })
    save_user_data(user_id, data)

def add_transcript(user_id, text):
    """
    Add a transcribed voice message to the user's session data.

    Args:
        text (str): speech-to-text result
    """
    data = load_user_data(user_id)
    data["transcripts"].append(text)
    save_user_data(user_id, data)

def log_interaction(user_id, user_input, ai_response):
    """
    Log both user question and assistant reply into history.

    Args:
        user_input (str): Message from user
        ai_response (str): Generated reply from AI
    """
    add_to_history(user_id, user_input, role="user")
    add_to_history(user_id, ai_response, role="assistant")