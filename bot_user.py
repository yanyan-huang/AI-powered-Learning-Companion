import os
import json
from datetime import datetime
from langchain.schema import BaseMessage 
# ======================== #
#  Bot User Class        #
# ======================== #
# This class encapsulates all state and behavior related to a specific user.
# It handles:
#   - Mode: Current active learning mode (mentor, coach, interviewer)
#   - Memory: The latest relevant turn-by-turn conversation used as context for the LLM
#   - History: A full, serialized log of all inputs/outputs (for review, analytics, future personalization)
#
# MEMORY vs. HISTORY (Key Design Difference)
# -------------------------------------------
# `memory` is used to construct prompts for LLMs (OpenAI, Gemini, Claude).
# It contains only recent, relevant messages in a format expected by LangChain or OpenAI APIs.
# Stored as `BaseMessage` objects, often trimmed to stay within token limits.
#
# `history` stores the full transcript of the conversation — every message, from both user and assistant.
# It includes timestamps, message roles, sources (text/voice), and mode context.
# Useful for logging, replaying, and analyzing conversations.
#
# This class ensures both are written to disk under a per-user JSON file inside `user_data/`.

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