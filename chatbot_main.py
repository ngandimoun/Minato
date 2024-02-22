# main file code for chatbot.py

import streamlit as st
from chat_openai_utils import get_openai_client
from chat_ui_components import configuration_expander, chat_history_expander, main_chat_interface
from chat_history_utils import load_chat_history, save_chat_history


def main():
    # Setup the Streamlit page
    #st.set_page_config(page_title="AI Chat Application", layout="wide")
    st.title("AI Chat Application")

    # Initialize session state variables if they don't exist
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = ""
    if "messages" not in st.session_state:
        st.session_state["messages"] = load_chat_history()

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    # UI Components
    configuration_expander()
    chat_history_expander(st.session_state["messages"])

    # Initialize the OpenAI client
    openai_client = get_openai_client()

    # Main chat interface
    main_chat_interface(openai_client, st.session_state["messages"])

    # Optional: Save chat history after each interaction
    save_chat_history(st.session_state["messages"])




    # Additional information or footer
    st.markdown("---")
    st.markdown("---")

    st.markdown("Developed with :heart: by [Chris NGANDIMOUN](https://yourwebsite.com)")

if __name__ == "__main__":
    main()
