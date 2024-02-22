import openai
import streamlit as st

def get_openai_client():
    """
    Initializes and returns the OpenAI client using the API key provided by the user.
    The API key is expected to be stored in the Streamlit session state.
    
    Returns:
        openai.Client: The initialized OpenAI client if the API key is available.
        None: If the API key is not set or missing.
    """
    api_key = st.session_state.get("api_key")
    if api_key:
        openai.api_key = api_key
        return openai
    else:
        st.error("Minato key is not set. Please enter your API key in the configuration.")
        return None
