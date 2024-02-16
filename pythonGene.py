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
    # Replace 'YOUR_OPENAI_API_KEY' with your actual Minato Key

    openai.api_key = os.getenv('OPENAI_API_KEY')
    return openai


#function to exect python code
def execute_python_code(code):
    # List of allowed libraries for the executed code
    allowed_libraries = [
        'pandas',  # Data Analysis
        'numpy',  # Scientific Computing, Array Manipulation
        'matplotlib',  # Data Visualization
        'requests',  # API Development, Web Scraping
        'asyncio',  # Concurrency
        'aiohttp',  # Asynchronous HTTP Client/Server
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

#define global model 
model="gpt-3.5-turbo-instruct"

# Function to diagnose issues in the user code
def diagnose_code_issues(code, problem_statement, sample_input):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Keys provided.")
        return "Error: No Minato Keys."

    if not code or not problem_statement:
        return "Code or problem statement is missing."

    combined_prompt = f"Based of Problem Statement: {problem_statement} and Sample input: {sample_input} \n\nPython Code:\n{code}\n\nDiagnose any issues with the code and explain them:"

    try:
        stream_response = client.completions.create(
            model=model,
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=250,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        
        
        full_response = stream_response.choices[0].text.strip()
        st.markdown(full_response, unsafe_allow_html=True)


    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"


# Function to give a  clean code solution

def clean_up_code(problem_statement, sample_input):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Keys provided.")
        return "Error: No Minato Keys."

    if not problem_statement:
        return "Code or problem statement is missing."


    combined_prompt = f"Based of Problem Statement: {problem_statement} and sample input example input: {sample_input} \n\nPython\n\nGive a clean code solution and Include sample input example:\n{sample_input}:"

    try:
        stream_response = client.completions.create(
            model=model,
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=500,
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
        st.error("No Minato Keys provided.")
        return

    combined_prompt = f"Create a {difficulty} level Python challenge related to {topic}. " \
                      f"Provide a problem statement, sample input, expected output, explanation and hint."

    try:
        stream_response = client.completions.create(
            model=model,
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=300,
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
    
    # Set company name for Streamlit app title
    #company_name = 'Your Very Long Company Name'

    # Set title with custom font color using markdown
    #font_color = '#FF5733'
    #st.markdown(f"<h1 style='text-align: center; font-size: 24px; color: {font_color};'>{company_name}</h1>", unsafe_allow_html=True)



    with st.expander("Configuration"):
        # Additional section for Discord and Email
        st.markdown("""
            - [🤑 Get Minato Free Credit](https://discord.gg/pNvPGqWfyX)

        """)
        
        st.markdown("""
    <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Please add your Minato Key</span>
    </h2>
    """, unsafe_allow_html=True)
    
        api_key = st.text_input("Enter your Minato Key", type="password")
        if api_key:
            st.session_state["api_key"] = api_key
        else:
            st.warning("Please enter your Minato Key.")
            
    st.caption('More  :blue[Programming] _Languages_  are coming soon :sunglasses:')

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
        code = st_ace.st_ace(language='python', keybinding=keybinding, theme=theme, placeholder="Write your code here...", height=400, key='code')



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

        # Display output if 'Run Code' button was clicked
        if run_clicked:
            output = execute_python_code(code)
      
            st.text_area("Output:", output, height=300)

        # Display diagnosis if 'What's wrong with my code?' button was clicked
        if diagnose_clicked:
            problem_statement = st.session_state.get('challenge', '')
            sample_input = st.session_state.get('challenge', '')
            diagnosis = diagnose_code_issues(code, problem_statement, sample_input)


        # Display cleaned code if 'Make my code clean' button was clicked
        if clean_clicked:
            problem_statement = st.session_state.get('challenge', '')
            sample_input = st.session_state.get('challenge', '')
            cleaned_code = clean_up_code(problem_statement, sample_input)




# Run the app
if __name__ == "__main__":
    main()
    
    
    
