import streamlit as st
import streamlit_ace as st_ace
from config import USER_AVATAR, BOT_AVATAR, DEFAULT_EDITOR_THEME, DEFAULT_KEYBINDING
from code_execution import execute_python_code
from coding_diagnostics import diagnose_code_issues, clean_up_code
from coding_challenges import generate_python_challenge

def configuration_expander():
    """
    Creates a UI component for API key configuration.
    """
    with st.expander("Configuration"):
        st.markdown("- [🤑 Get Minato Free Credit](https://discord.gg/pNvPGqWfyX)")
        api_key = st.text_input("Enter your Minato Key", type="password")
        if api_key:
            st.session_state["api_key"] = api_key
            st.success("API Key updated!")
        else:
            st.warning("Please enter your Minato Key.")

def python_challenge_ui():
    """
    UI for generating and displaying Python challenges.
    """
    st.markdown("""
    <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Python Challenge</span>
    </h2>
    """, unsafe_allow_html=True)
    difficulty = st.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Hard", "Expert"], key='difficulty')

    # Enhanced list of Python-specific topics
    python_topics = [
        # Fundamentals
        "Math Operations", "Data Structures", "String Manipulation", "Array Manipulation",
        "Error Handling", "Regular Expressions",

        # Intermediate Concepts
        #"Decorators in Python", "Generators and Iterators", "Context Managers",
        "Lambda Functions", "List Comprehensions", "Exception Handling",

        # Advanced Python Topics
        "Algorithms", "Binary Search", "Functional Programming", "Object-Oriented Programming",

        "Scripting with Python", "Building Command Line Interfaces",

        # Scientific and Numeric Computing
        "Scientific Computing with NumPy", # "Statistical Analysis with SciPy",
        "Symbolic Mathematics with SymPy",

        # Blockchain and Cryptocurrency
        "Blockchain Fundamentals with Python", "Smart Contracts with Python",
        

        # Cybersecurity
        "Python for Network Security", "Penetration Testing with Python",
        "Cryptographic Techniques in Python",

        # Other
        #"Geospatial Analysis with GeoPandas", "Web Application Security Testing", "Cryptocurrency Data Analysis",
    ]

    topic = st.selectbox("Select Topic", python_topics, key='topic')


    if st.button("Generate"):
        generate_python_challenge(difficulty, topic)
        # Display the challenge if it's stored in the session state
    if 'challenge' in st.session_state:
        st.markdown(st.session_state['challenge'], unsafe_allow_html=True)       

def python_code_executor_ui():
    """
    UI for executing, diagnosing, and cleaning up Python code.
    """
    st.markdown("""
    <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Python Code Executor</span>
    </h2>
    """, unsafe_allow_html=True)
    with st.expander("Customize Editor"):

        theme = st.selectbox(
                        'Select Theme',
                        ('ambiance', 'chaos', 'chrome', 'clouds', 'clouds_midnight', 'cobalt', 'crimson_editor', 'dawn', 'dracula', 
                        'dreamweaver', 'eclipse', 'github', 'gob', 'gruvbox', 'idle_fingers', 'iplastic', 'katzenmilch', 'kr_theme', 
                        'kuroir', 'merbivore', 'merbivore_soft', 'mono_industrial', 'monokai', 'nord_dark', 'pastel_on_dark', 
                        'solarized_dark', 'solarized_light', 'sqlserver', 'terminal', 'textmate', 'tomorrow', 'tomorrow_night', 
                        'tomorrow_night_blue', 'tomorrow_night_bright', 'tomorrow_night_eighties', 'twilight', 'vibrant_ink', 'xcode'),
                        index=32)  # Default to 'tomorrow_night_blue'

        # Editor keybinding selection
        keybinding = st.selectbox(
            'Select Keybinding',
            ('ace', 'vim', 'emacs', 'sublime', 'vscode', 'textmate'),
            index=4)  # Default to 'vscode'

    code = st_ace.st_ace(language='python', keybinding=keybinding, theme=theme, placeholder="Write your code here...", height=400)
    
    st.caption('Click first on  :blue[Apply] before _Run code_  and others :sunglasses:')


    # Flags to track which button has been pressed
    run_clicked = False
    diagnose_clicked = False
    clean_clicked = False

    # Creating a row of columns for the buttons
    col_run, col_diagnose, col_clean = st.columns(3)

    with col_run:
        run_clicked = st.button('Run My Code')

    with col_diagnose:
        diagnose_clicked = st.button("Diagnose My Code")

    with col_clean:
        clean_clicked = st.button("Clean Code Solution")


    if run_clicked:
        output = execute_python_code(code)
        st.text_area("Output:", output, height=150)


    if diagnose_clicked:
        problem_statement = st.session_state.get('challenge', '')
        sample_input = st.session_state.get('challenge', '')
        diagnosis = diagnose_code_issues(code, problem_statement, sample_input)
        st.markdown(diagnosis, unsafe_allow_html=True)


    if clean_clicked:
        problem_statement = st.session_state.get('challenge', '')
        sample_input = st.session_state.get('challenge', '')
        cleaned_code = clean_up_code(problem_statement, sample_input)
        st.markdown(cleaned_code, unsafe_allow_html=True)

