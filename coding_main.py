import streamlit as st
from coding_ui_components import configuration_expander, python_challenge_ui, python_code_executor_ui
from coding_config import USER_AVATAR, BOT_AVATAR

def main():
    # Set up the page configuration and title
    #st.set_page_config(page_title="Python Code Assistant", layout="wide")
    st.title("Python Code Simulation")

    # Configuration UI for entering the OpenAI API key
    configuration_expander()

    # Display a warning if the API key is not set
    if "api_key" not in st.session_state or not st.session_state["api_key"]:
        st.warning("Please enter your OpenAI API key in the Configuration section.")

    # UI components for Python challenges and code execution
    col1, col2 = st.columns(2)
    with col1:
        python_challenge_ui()

    with col2:
        python_code_executor_ui()

    # Additional information or footer
    st.markdown("---")
    st.markdown("---")

    st.markdown("Developed with :heart: by [Chris NGANDIMOUN](https://yourwebsite.com)")

if __name__ == "__main__":
    main()
