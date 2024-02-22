# chat_history_utils.py for chatbot.py
# Utility functions for managing chat history

import shelve

def load_chat_history():
    """Loads chat history from a shelve file."""
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

def save_chat_history(messages):
    """Saves chat history to a shelve file."""
    with shelve.open("chat_history") as db:
        db["messages"] = messages
