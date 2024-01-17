# Import necessary libraries hello world hello again
import streamlit as st
import streamlit_ace as st_ace
import html
import openai
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import os
import random
import json
from openai import OpenAI
import subprocess
#import mimetypes
import time
import shutil
import stat
import pickle
from pathlib import Path
import git

import re

st.set_page_config(layout="wide")



# Custom CSS to increase the width of the main content area
def set_css_to_increase_width():
    st.markdown(
        """
        <style>
        .reportview-container .main .block-container{
            max-width: 90%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

set_css_to_increase_width()





# OpenAI client setup

def get_openai_client():
    """
    Create an OpenAI client using the API key provided by the user.
    """
    api_key = st.session_state.get("api_key")
    if api_key:
        return openai.Client(api_key=api_key)
    else:
        return None
        

@st.cache_data(ttl=3600, show_spinner=False)
def generate_query_response(user_query, code_context):
    try:
    
        client = get_openai_client()
        if client is None:
            return "No OpenAI API key provided."
        # Determine the language from the code context or user query
        language = determine_language(code_context, user_query)

        combined_prompt = (
            f"Code Context:\n{code_context}\n\n"
            f"Question: {user_query}\n\n"
            "Answer:"
        )
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.7,
            max_tokens=550,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Format the response
        formatted_response = format_response(response.choices[0].text.strip(), language)
        
        return formatted_response
    except Exception as e:
        return str(e)

        


def format_response(response, language):
    """
    Formats the response so that each sentence is on a new line.

    Parameters:
    response (str): The response text to be formatted.
    language (str): The language of the code.

    Returns:
    str: The formatted response.
    """
    # Split the response into sentences
    sentences = re.split(r'(?<=[.!?]) +', response)

    # Join the sentences with a newline character
    formatted_response = '\n'.join(sentences)

    # Check if the response is too long for a single line
    if len(formatted_response.split('\n')) > 1 or len(formatted_response) > 80:
        # Multi-line or long response
        return f"```{language}\n{formatted_response}\n```"
    else:
        # Single-line response, add indentation for better readability
        return f"```{language}\n    {formatted_response}\n```"
        




def determine_language(code_context, user_query):
    """
    Determine the programming language from the code context or user query.

    Parameters:
    code_context (str): The code context or background information.
    user_query (str): The user's query.

    Returns:
    str: The identified language code for formatting.
    """
    # A mapping of keywords to language codes for formatting
    language_map = {
        'py': 'python', 'js': 'javascript', 'css': 'css', 
        'cpp': 'cpp', 'dart': 'dart', 'java': 'java', 
        'sol': 'solidity', 'php': 'php', 'cs': 'csharp', 
        'go': 'go', 'rb': 'ruby', 'sql': 'sql', 
        'swift': 'swift', 'kt': 'kotlin', 'html': 'html'
    }

    # Logic to determine the language from code_context or user_query
    # This is a placeholder, and you might need a more sophisticated method
    for key, value in language_map.items():
        if key in code_context or key in user_query:
            return value

    # Default to 'text' if no specific language is identified
    return 'text'

def handle_query(user_query, code_context):
    if user_query:
        query_result = generate_query_response(user_query, code_context)
        formatted_query = format_response(f" {user_query}", 'text')
        formatted_response = format_response(f" {query_result}", 'text')
        st.session_state.chat_history.append({"question": formatted_query, "answer": formatted_response})
        return query_result
    return ""
    
   
    
def main():
    
     # Add an icon from an online source
    # Hid this icon and added it to the next line copying onboard.app
    #st.image("https://www.pngitem.com/pimgs/m/90-903305_naruto-kunai-minato-freetoedit-hd-png-download.png", width=100)
    
    #st.title("🗡️ Minato: Search, learn & edit 1000+ file codebases")
    st.title("🗡️ Minato")
    st.text("AI expert on any codebase")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    st.text("Step 1: Upload your own files or enter the link to any GitHub repo")
    st.markdown("\n")
    st.text("Step 2: Select the files you'd like to work with.")
    st.markdown("\n")
    st.text("Step 3: Chat with Minato to understand, navigate, and generate code for selected files.")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
    st.markdown("\n")
   
    
    # CSS styling
    st.markdown("""
        <style>
        .chatbox {
            border: 2px solid #008CBA;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            background-color: #f1f1f1;
        }
        .chat-message {
            font-family: Arial, sans-serif;
            padding: 5px;
            margin: 4px 0;
            border-radius: 5px;
        }
        .user-message {
            background-color: #dff0d8;
            border: 1px solid #d6e9c6;
            color: #3c763d;
        }
        .bot-message {
            background-color: #d9edf7;
            border: 1px solid #bce8f1;
            color: #31708f;
        }
        .message-content {
            white-space: pre-line;
        }
        .question {
            font-weight: bold;
            color: #555;
        }
        .answer {
            font-weight: bold;
            color: #000;
        }
        </style>
    """, unsafe_allow_html=True)


        
    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        
        




    # File uploader for various code file types
    file_types = ["py", "js", "css", "cpp", "dart", "java", "sol", "php", "cs", "go", "rb", "sql", "swift", "kt", "html", "txt", "md"]
    #st.markdown("## Step 1: Enter the link to any GitHub repo or upload your own repo.")
    #st.caption("Upload your code files here. Supported formats include Python, JavaScript, CSS, C++, Dart, Java, and more. View the contents of uploaded files in the next section.")

    uploaded_files = st.file_uploader("Step 1. Upload your own files", type=file_types, accept_multiple_files=True)
    


    # Extract content from uploaded files
    code_context = ""
    for file in uploaded_files:
        file_content = file.getvalue().decode("utf-8")
        code_context += f"\n\nFile Name: {file.name}\n{file_content}"   
    


    if uploaded_files:
    

        # Limit the selection to a maximum of 4 files
        selected_files = st.multiselect("Select files to display", [f.name for f in uploaded_files], default=[f.name for f in uploaded_files][:4])

        if selected_files:
            # Display files in rows of up to 4 columns
            for i in range(0, len(selected_files), 4):
                row_files = selected_files[i:i + 4]
                columns = st.columns(len(row_files))

                for col, file_name in zip(columns, row_files):
                    with col:
                        file = next(f for f in uploaded_files if f.name == file_name)
                        code = file.getvalue().decode("utf-8")
                        file_extension = file.name.split('.')[-1]
                        language_map = {
                            'py': 'python', 'js': 'javascript', 'css': 'css', 'cpp': 'c_cpp', 'dart': 'dart',
                            'java': 'java', 'sol': 'solidity', 'php': 'php', 'cs': 'csharp', 'go': 'golang',
                            'rb': 'ruby', 'sql': 'sql', 'swift': 'swift', 'kt': 'kotlin', 'html': 'html'
                            }
                        language = language_map.get(file_extension, 'text')

                        # Use st_ace without 'use_container_width'
                        st_ace.st_ace(
                            language=language,
                            value=code,
                            theme="twilight",
                            key=f"ace-editor-{file.name}",
                            readonly=True,
                            height=300
                            
                        )
                        
    def on_rm_error(func, path, exc_info):
        # Remove read-only attributes and retry
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    def clear_directory(directory):
        if os.path.exists(directory):
            for _ in range(5):  # Retry loop
                try:
                    shutil.rmtree(directory, onerror=on_rm_error)
                    os.makedirs(directory)
                    return
                except Exception as e:
                    print(f"Attempt to clear directory failed: {e}")
                    time.sleep(1)  # Wait a bit for any locks to be released
        else:
            os.makedirs(directory)  # Create directory if it doesn't exist

        raise Exception(f"Unable to clear the directory: {directory}")
        
    
    # Function to clone git repository


    def clone_git_repo(repo_url, destination):
        try:
        
            # Clear the destination directory before cloning
            clear_directory(destination)
            
            git.Repo.clone_from(repo_url, destination)
            return "Repository cloned successfully."
        except Exception as e:
            return f"Error cloning repository: {e}"
            
            



    def list_files_recursively(directory):
        all_files = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                all_files[relative_path] = os.path.join(root, file)
        return all_files

    def filter_files(search_query, file_list):
        if not search_query:
            return file_list
        return [file for file in file_list if search_query.lower() in file.lower()]


    # Streamlit UI st.subheader("🌌: Clone Git Repository")
    
    st.text("or")
    repo_url = st.text_input("Step 1 Enter the link to any GitHub repo")
    destination = "path/to/clone"  # You might consider making this a user input

    if st.button("Clone Repository"):
        message = clone_git_repo(repo_url, destination)
        st.write(message)





    # Function to list files and directories in a directory
    def list_files_and_dirs(directory):
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))], \
               [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    if 'current_path' not in st.session_state:
        st.session_state['current_path'] = destination

    def update_path(new_path):
        st.session_state['current_path'] = new_path



    st.markdown("### Examine the Names of Directories and Files.")
    def file_explorer(path):
        files, dirs = list_files_and_dirs(path)

        if path != destination and st.button('Go up'):
            update_path(os.path.dirname(path))
        
        with st.expander("Directories Names"):
            for d in dirs:
                if st.button(f"📁 {d}"):
                    update_path(os.path.join(path, d))

        selected_files = st.multiselect("FIles Names", files)

        if selected_files:
            for selected_file in selected_files:
                file_path = os.path.join(path, selected_file)


    file_explorer(st.session_state['current_path'])




    repo_files = {}
    if os.path.exists(destination):
        repo_files = list_files_recursively(destination)

    
    # Live search implementation
    search_query = st.text_input("Search for Files or Input Specific Names", key="search")

    if repo_files:
        filtered_files = filter_files(search_query, list(repo_files.keys()))
        selected_files_paths = st.multiselect("Select Files to Display", filtered_files, format_func=lambda x: x.split('/')[-1])

        code_context = ""
        if selected_files_paths:
            num_columns = len(selected_files_paths)
            if num_columns > 0:
                columns = st.columns(num_columns)

                for i, file_path in enumerate(selected_files_paths):
                    with open(repo_files[file_path], "r") as file:
                        file_content = file.read()
                        file_extension = file_path.split('.')[-1]
                        language_map = {
                            'py': 'python', 'js': 'javascript', 'css': 'css', 'cpp': 'c_cpp', 'dart': 'dart',
                            'java': 'java', 'sol': 'solidity', 'php': 'php', 'cs': 'csharp', 'go': 'golang',
                            'rb': 'ruby', 'sql': 'sql', 'swift': 'swift', 'kt': 'kotlin', 'html': 'html'
                            }
                        language = language_map.get(file_extension, 'text')

                        with columns[i]:
                            st_ace.st_ace(language=language, value=file_content, theme="twilight", key=f"ace-editor-{file_path}", readonly=True, height=300)

                        # Append file content to code_context for further processing
                        code_context += f"\n\nFile Path: {file_path}\nFile Content:\n{file_content}"



    with st.sidebar:
        # Additional section for Discord and Email
        st.write("## Get more Minato products")
        st.markdown("""
            - [🤑 Get Minato Free Open AI Credit](https://discord.gg/pNvPGqWfyX)
            - [VSCode Extension: Get early access!](https://forms.gle/1Zs4NcsscFp9pxM77)
        """)
        st.write("## Please add your API Key to use Minato API")
        api_key = st.text_input("Enter your OpenAI API key or Minato free GPT Credit", type="password")
        if api_key:
            st.session_state["api_key"] = api_key
        else:
            st.warning("Please enter your OpenAI API key.")
            
        st.markdown("### Chat History")
        for chat in st.session_state.chat_history:
            st.markdown(chat['question'], unsafe_allow_html=True)
            st.markdown(chat['answer'], unsafe_allow_html=True)

        if st.button("Clear History", key="clear_history_button"):
            st.session_state.chat_history = []
            
            
    
    



    # Chatbot-like interface on the main page
    st.markdown("### Step 2: Chat with Minato to understand, navigate, and generate code for the repo.")
    
    
    # Sample questions
    sample_questions = [
        "How do I implement a binary search in Python?",
        "What are the differences between let and var in JavaScript?",
        "How can I center a div in CSS?",
        "What is the use of async/await in JavaScript?",
        "I'm working on a React component in JavaScript that interacts with an API. Could you provide a basic test script using Jest and React Testing Library? The test should check if the component renders and handles API data correctly.",
        "I have a Java class with several methods that perform various operations. Could you show me how to write JUnit test cases for one of these methods? The test should include checks for valid inputs, handling of invalid inputs, and ensuring the method behaves as expected."
    ]


    # Function to handle question
    def handle_sample_question(question):
        # Update the query in the session state
        st.session_state.user_query = question
        # Assuming 'handle_query' is the function that processes the question
        response = handle_query(question, code_context)
        st.session_state.response = response

    # Creating a 2x2 grid for sample questions
    col1, col2 = st.columns(2)
    with col1:
        if st.button(sample_questions[0]):
            handle_sample_question(sample_questions[0])
        if st.button(sample_questions[2]):
            handle_sample_question(sample_questions[2])
        if st.button(sample_questions[4]):
            handle_sample_question(sample_questions[4])
        
    with col2:
        if st.button(sample_questions[1]):
            handle_sample_question(sample_questions[1])
        if st.button(sample_questions[3]):
            handle_sample_question(sample_questions[3])
        if st.button(sample_questions[5]):
            handle_sample_question(sample_questions[5])
        


    # Text input for user query
    # If user_query is in session state, use it as the default value
    #user_query = st.text_input("", value=st.session_state.get('user_query', ''), placeholder="Type your question here...", key="query_input")

    # Check if the user manually submits a query
#if st.button("Submit"):
  #      if user_query:
   #         handle_query(user_query, code_context)



    query_col, button_col = st.columns([0.9, 0.1])

    with query_col:
        user_query = st.text_area("", value=st.session_state.get('user_query', ''), 
                                  placeholder="Type your question here...", key="query_input", height=100)

    with button_col:
        if st.button("🔍", key="query_submit_button"):
            if user_query:
                handle_query(user_query, code_context)
                with st.spinner('Waiting for response...'):
                    response = handle_query(user_query, code_context)
                    st.session_state.response = response






    # Display the response
    if 'response' in st.session_state and st.session_state.response:
        st.markdown(f"**MinatoMinato:**\n{st.session_state.response}")


if __name__ == "__main__":
    main()





# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
