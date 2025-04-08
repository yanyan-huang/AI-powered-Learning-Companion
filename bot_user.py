import os
import json
from datetime import datetime
from langchain.schema import BaseMessage 
# ======================== #
#  Bot User Class        #
# ======================== #
# This class handles user data, including mode, memory, and interaction history.
# It loads and saves user data to a JSON file, allowing for persistent storage.
# The class is initialized with a user ID and manages the user's mode and memory.
# It also logs interactions with timestamps and sources.
# The class is designed to be used in a Telegram bot context, where user data needs to be stored and retrieved.
# It creates a directory for user data if it doesn't exist and handles loading and saving of user data.
# It raises errors if the user ID is invalid or if there are issues with file operations.
# It provides methods for getting and updating memory, logging interactions, and managing the user's mode.

USER_DATA_DIR = "user_data"
os.makedirs(USER_DATA_DIR, exist_ok=True)

class BotUser:
    def __init__(self, user_id):
        """Initialize the BotUser with a user ID and load user data."""
        self.user_id = str(user_id)
        self.filepath = os.path.join(USER_DATA_DIR, f"{self.user_id}.json")
        self.data = self._load_data()

    def _load_data(self):
        """Load user data from a JSON file or create a new one if it doesn't exist."""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        else:
            return {"mode": None, "memory": {}, "history": []}

    def save(self):
        """Save user data to a JSON file."""
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=2)

    @property
    def mode(self):
        """Get the current mode of the user."""
        return self.data.get("mode")

    @mode.setter
    def mode(self, value):
        """Set the current mode of the user and save the data."""
        self.data["mode"] = value
        self.save()

    def get_memory(self):
        """Get the memory for the current mode."""
        return self.data.get("memory", {})

    def update_memory(self, mode, memory):
        """Update the memory for the current mode and save the data."""
        # Serialize messages to dicts
        serializable_memory = {}
        for m, messages in memory.items():
            serializable_memory[m] = [
                {"type": msg.type, "content": msg.content} if isinstance(msg, BaseMessage) else msg
                for msg in messages
            ]
        self.data["memory"] = serializable_memory
        self.save()

    def log_interaction(self, user_input, ai_reply, source="text"):
        """Log the interaction with a timestamp and source."""
        timestamp = datetime.utcnow().isoformat()
        self.data["history"].append({"role": "user", "content": user_input, "timestamp": timestamp, "source": source, "mode": self.mode})
        self.data["history"].append({"role": "assistant", "content": ai_reply, "timestamp": timestamp, "source": "text", "mode": self.mode})
        self.save()