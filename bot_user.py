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

import os
# import json
from datetime import datetime
from langchain.schema import BaseMessage
from firebase_db import db # This import is for Firebase Firestore database connection 

USER_DATA_DIR = "user_data"
os.makedirs(USER_DATA_DIR, exist_ok=True)

class BotUser:
    def __init__(self, user_id):
        # """Initialize the BotUser with a user ID and load user data from disk."""
        """Initialize the BotUser with a user ID and Firebase Firestore document reference."""
        self.user_id = str(user_id)
        self.doc_ref = db.collection("users").document(self.user_id)

    def _load_or_init_profile(self):
        """Load or initialize the user profile in Firestore."""
        doc = self.doc_ref.get()
        if not doc.exists:
            self.doc_ref.set({
                "mode": None,
                "created_at": datetime.utcnow().isoformat()
            })
        return self.doc_ref.get().to_dict()
    
    @property
    def mode(self):
        """Get the current mode of the user from the loaded profile in Firestore."""
        profile = self._load_or_init_profile()
        return profile.get("mode")

    @mode.setter
    def mode(self, value):
        """Set the current mode of the user and update it in Firestore."""
        self.doc_ref.update({
            "mode": value,
            "last_active": datetime.utcnow().isoformat()
        })

    def get_memory(self):
        """Retrieve the user's conversational memory from Firestore."""
        mem_docs = self.doc_ref.collection("memory_snapshots").stream()
        return {
            doc.id: doc.to_dict().get("messages", [])
            for doc in mem_docs
        }

    def update_memory(self, mode, memory):
        """
        Update and persist the memory used to construct prompts for the LLM.
        Each message must be serialized so it's JSON-safe.
        """
        messages = []
        for msg in memory.get(mode, []):
            if isinstance(msg, BaseMessage):
                role = "user" if msg.type == "human" else msg.type  # Normalize 'human' → 'user'
                messages.append({
                    "role": role,  # ← explicitly renaming `type` → `role` as category
                    "content": msg.content
                })
            elif isinstance(msg, dict) and "role" in msg:
                messages.append(msg)

        self.doc_ref.collection("memory_snapshots").document(mode).set({
            "messages": messages,
            "updated_at": datetime.utcnow().isoformat()
        })

    def log_interaction(self, user_input, ai_reply, source="text", system_message=None):
        """
        Log a user interaction into the persistent history log in Firestore.
        Includes user and AI messages, timestamp, and source (text/voice).
        - Optionally includes a system message
        - Each message includes a role: 'system', 'user', or 'ai'
        """
        entries = []

        if system_message:
            entries.append({
                "role": "system",
                "content": system_message
            })

        entries.append({
            "role": "user",
            "content": user_input
        })

        entries.append({
            "role": "ai",
            "content": ai_reply
        })

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "mode": self.mode,
            "source": source,  # 'text' or 'voice'
            "entries": entries
        }

        self.doc_ref.collection("history_logs").add(entry)


    def log_metric_event(self, event_name="session_interaction"):
        """
        Save a minimal metric entry to Firestore.
        Logs the user's current mode and timestamp.
        """
        print("📊 Logging minimal metric event to Firestore...")
        self.doc_ref.collection("metrics").add({
            "event": event_name,
            "mode": self.mode,
            "timestamp": datetime.utcnow().isoformat()
        })


    def get_llm_usage_count(self):
        """
        Retrieve the LLM usage count from Firestore.
        Returns the count of LLM interactions for this user.
        """
        doc = self.doc_ref.collection("metrics").document("llm_usage").get()
        return doc.to_dict().get("count", 0) if doc.exists else 0

    def increment_llm_usage_count(self):
        """
        Increment the LLM usage count in Firestore.
        This is used to track how many times the LLM has been used by this user.
        """
        usage_ref = self.doc_ref.collection("metrics").document("llm_usage")
        doc = usage_ref.get()
        current = doc.to_dict().get("count", 0) if doc.exists else 0
        usage_ref.set({"count": current + 1})
