import streamlit as st
import openai
import os
import streamlit_ace as st_ace
import contextlib
import io
import sys
import subprocess
import uuid
import importlib
from openai import OpenAI


# Define the function to get the OpenAI client
def get_openai_client():
    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key

    openai.api_key = os.getenv('OPENAI_API_KEY')
    return openai


def execute_python_code(code):

    allowed_libraries = [
        'pandas',  # Data Analysis
        'numpy',  # Scientific Computing, Array Manipulation
        'matplotlib',  # Data Visualization
        'scipy',  # Scientific Computing, used with NumPy
        'flask',  # Web Development
        'django',  # Web Development
        'requests',  # API Development, Web Scraping

        'lxml',  # Web Scraping, Parsing XML and HTML
        'pytest',  # Testing
        'asyncio',  # Concurrency
        'aiohttp',  # Asynchronous HTTP Client/Server
        'tkinter',  # GUI Development (note: it's a standard library, so it might not need to be in this list)
        'pygame',  # Game Development
        'pyqt5',  # GUI Development
        'pyopengl',  # Game Development, Graphics

        'pyautogui',  # GUI Automation
        're',  # Regular Expressions (note: it's a standard library)
        'socket',  # Network Programming (note: it's a standard library)
        'os',  # File I/O, Operating System Interaction (note: it's a standard library)
        'json',  # Working with JSON Data (note: it's a standard library)
        'csv',  # File I/O for CSV files (note: it's a standard library)
        'time',  # Timing and Delays (note: it's a standard library)
        'streamlit'  # Web App Development for Data Science
    ]

    output = io.StringIO()

    # Extracting imported modules from the code
    imported_modules = []
    for line in code.split('\n'):
        if line.startswith('import'):
            imported_modules.extend(line.split()[1].split(','))
        elif line.startswith('from'):
            imported_modules.append(line.split()[1])

    # Checking if any imported module is not allowed
    for module in imported_modules:
        if module.split('.')[0] not in allowed_libraries:
            return f"Error: Importing library '{module}' not allowed."

    # Creating a restricted global environment with allowed libraries
    global_env = {'__builtins__': __builtins__}
    for lib in allowed_libraries:
        global_env[lib] = importlib.import_module(lib)

    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            exec(code, global_env)
    except Exception as e:
        output.write(f'Error: {e}')

    return output.getvalue()




# Function to diagnose issues in the code
def diagnose_code_issues(code, problem_statement):
    client = get_openai_client()
    if client is None:
        st.error("No OpenAI API key provided.")
        return "Error: No OpenAI API key."

    if not code or not problem_statement:
        return "Code or problem statement is missing."

    combined_prompt = f"Problem Statement: {problem_statement}\n\nPython Code:\n{code}\n\nDiagnose any issues with the code and explain them:"

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```python\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"


# Function to clean up the code
def clean_up_code(code, problem_statement):
    client = get_openai_client()
    if client is None:
        st.error("No OpenAI API key provided.")
        return "Error: No OpenAI API key."

    if not code or not problem_statement:
        return "Code or problem statement is missing."

    combined_prompt = f"Problem Statement: {problem_statement}\n\nPython Code:\n{code}\n\nRefactor the code to make it cleaner and more efficient:"

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```python\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"



# Define the function to generate a Python challenge
def generate_challenge(difficulty, topic):
    full_response = ""
    message_placeholder = st.empty()

    client = get_openai_client()
    if client is None:
        st.error("No OpenAI API key provided.")
        return

    combined_prompt = f"Create a {difficulty} level Python challenge related to {topic}. " \
                      f"Provide a problem statement, sample input, expected output, explanation and hint."

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=180,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            
        )

        full_response = stream_response.choices[0].text.strip()


        sections = full_response.split('\n\n')

        # Separate labels and contents for each section
        problem_statement_label, problem_statement_content = sections[0].split(':', 1)
        sample_input_label, sample_input_content = sections[1].split(':', 1)
        expected_output_label, expected_output_content = sections[2].split(':', 1)
        explanation_output_label, explanation_output_content = sections[3].split(':', 1)
        hint_output_label, hint_output_content = sections[4].split(':', 1)

        colored_response = f"""
            <p><span style='color: red;'>{problem_statement_label}:</span>{problem_statement_content}</p> <!-- Problem Statement -->
            <p><span style='color: blue;'>{sample_input_label}:</span>{sample_input_content}</p> <!-- Sample Input -->
            <p><span style='color: green;'>{expected_output_label}:</span>{expected_output_content}</p> <!-- Expected Output -->
            <p><span style='color: orange;'>{explanation_output_label}:</span>{explanation_output_content}</p> <!-- Explanation Output -->
            <p><span style='color: violet;'>{hint_output_label}:</span>{hint_output_content}</p> <!-- Hint Output -->
        """
            

        # Store the colored response directly in the session state
        st.session_state['challenge'] = colored_response

    except Exception as e:
        st.error(f"An error occurred: {e}")    


# Main function for the Streamlit app
def main():
    #st.set_page_config(layout="wide")


    col1, col2 = st.columns(2)

    with col1:

 
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
            "File I/O", "Error Handling", "Regular Expressions",

            # Intermediate Concepts
            "Decorators in Python", "Generators and Iterators", "Context Managers",
            "Lambda Functions", "List Comprehensions", "Exception Handling",

            # Advanced Python Topics
            "Algorithms", "Binary Search", "Functional Programming", "Object-Oriented Programming",
            "Concurrency with asyncio", "Testing with PyTest", "Network Programming",
            "Metaprogramming", "Memory Management", "Python C Extensions",

            # Web Development
            "Web Scraping", "Web Development with Flask/Django", "API Development",
            "Template Engines (Jinja2)", "WSGI and ASGI Concepts",

            # Data Analysis and Visualization
            "Data Analysis with Pandas", "Data Cleaning", "Data Visualization with Matplotlib",
            "Data Manipulation with SQLAlachemy", "Advanced Data Visualization with Seaborn",

            # Application and Scripting
            "Automation Scripts", "GUI Development with Tkinter", "Game Development with Pygame",
            "Scripting with Python", "Building Command Line Interfaces",

            # Scientific and Numeric Computing
            "Scientific Computing with NumPy", "Statistical Analysis with SciPy",
            "Symbolic Mathematics with SymPy",

            # Blockchain and Cryptocurrency
            "Blockchain Fundamentals with Python", "Smart Contracts with Python",
            "Decentralized Applications (DApps) Development", "Cryptocurrency Data Analysis",

            # Cybersecurity
            "Python for Network Security", "Penetration Testing with Python",
            "Cybersecurity Automation with Python", "Web Application Security Testing",
            "Cryptographic Techniques in Python", "Incident Response with Python",

            # Other
            "Microservices in Python", "Web Crawling",
            "Geospatial Analysis with GeoPandas"
        ]

        topic = st.selectbox("Select Topic", python_topics, key='topic')


        if st.button("Minato"):
            generate_challenge(difficulty, topic)

        # Display the challenge if it's stored in the session state
        if 'challenge' in st.session_state:
            st.markdown(st.session_state['challenge'], unsafe_allow_html=True)


    with col2:

        
        st.markdown("""
        <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Python Code Executor</span>
        </h2>
        """, unsafe_allow_html=True)        
        #code = st_ace.st_ace(language='python', keybinding="vscode", theme='tomorrow_night_blue', height=300, key='code')


        # Use an expander for theme and editor options
        with st.expander("Customize Editor"):
            # Theme selection
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
                
                
        # ACE editor
        code = st_ace.st_ace(language='python', keybinding=keybinding, theme=theme, placeholder="Write your code here...", height=350, key='code')



        st.caption('Click first on  :blue[Apply] before _Run code_  and others :sunglasses:')

        st.sidebar.write("Close the navigation sidebar for a better viewing experience.")

        # Flags to track which button has been pressed
        run_clicked = False
        diagnose_clicked = False
        clean_clicked = False

        # Creating a row of columns for the buttons
        col_run, col_diagnose, col_clean = st.columns(3)

        with col_run:
            run_clicked = st.button('Run Code')

        with col_diagnose:
            diagnose_clicked = st.button("Code Checking")

        with col_clean:
            clean_clicked = st.button("Clean Code")

        # Display output if 'Run Code' button was clicked
        if run_clicked:
            output = execute_python_code(code)

            
            st.text_area("Output:", output, height=300)

        # Display diagnosis if 'What's wrong with my code?' button was clicked
        if diagnose_clicked:
            problem_statement = st.session_state.get('challenge', '')
            diagnosis = diagnose_code_issues(code, problem_statement)
            #st.text_area("Diagnosis:", diagnosis, height=150)

        # Display cleaned code if 'Make my code clean' button was clicked
        if clean_clicked:
            problem_statement = st.session_state.get('challenge', '')
            cleaned_code = clean_up_code(code, problem_statement)
            #st.text_area("Cleaned Code:", cleaned_code, height=150)



# Run the app
if __name__ == "__main__":
    main()
    
    
    
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)