# ui_components.py for chatbot.py
# Streamlit UI component functions
import openai
import streamlit as st
from chat_openai_utils import get_openai_client

# Assuming USER_AVATAR and BOT_AVATAR are defined in config.py or directly in this script

from chat_history_utils import save_chat_history, load_chat_history
from chat_cs_question_utils import is_computer_science_related
from chat_config import USER_AVATAR, BOT_AVATAR
import os
import shelve

DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
# Set up OpenAI client
client = get_openai_client()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

def configuration_expander():
    """
    Creates a UI component for API key configuration.
    """
    with st.expander("Configuration"):
        # Directly use session_state to get and set the API key
        new_api_key = st.text_input("Enter your API Key:", value=st.session_state.get("api_key", ""), type="password")
        if new_api_key:
            st.session_state["api_key"] = new_api_key
            st.success("API Key updated!")
        else:
            st.warning("Please enter a valid API Key.")

def chat_history_expander():
    """
    Creates a UI component for managing chat history.
    """
    with st.expander("Chat History"):
        if st.button("Delete Chat History"):
            st.session_state["messages"] = []  # Clear the chat history in the session state
            st.success("Chat history deleted!")


def main_chat_interface(openai_client, messages):
    """
    Creates the main chat interface for the application, using the provided OpenAI client
    and the current chat messages.
    
    Parameters:
    - openai_client: The OpenAI client to use for generating responses.
    - messages: The current chat messages list to be updated with new interactions.
    """
    
    # Display chat messages
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
        
# Main chat interface with topic detection
    if prompt := st.chat_input("Ask Minato, your Software Questions??"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)
               
                
        if is_computer_science_related(prompt):
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                message_placeholder = st.empty()
                full_response = ""
                for response in client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=st.session_state["messages"],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.content or ""
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                non_cs_response = "Sorry, this is not a computer science related question. Please ask something related to computer science."
                st.markdown(non_cs_response)
                st.session_state.messages.append({"role": "assistant", "content": non_cs_response})






