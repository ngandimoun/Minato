# openai_utils.py for chatbot.py
# OpenAI API client utility functions

import openai
import streamlit as st
from chat_config import DEFAULT_OPENAI_MODEL

def get_openai_client():
    """Retrieves the OpenAI client using the API key stored in session state."""
    api_key = st.session_state.get("api_key")
    if api_key:
        return openai.Client(api_key=api_key)
    else:
        return None
