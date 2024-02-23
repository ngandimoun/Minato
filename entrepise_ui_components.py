#UI components config for entreprise_software.py

#ui_components.py: Houses Streamlit UI components and the main application logic

import streamlit as st
import streamlit_ace as st_ace
import os
from entreprise_git_operations import clone_git_repo
from entreprise_file_management import generate_tree_structure, list_files_recursively

from entreprise_openai_integration import (get_openai_client, generate_documentation, generate_clean, 
                                diagnose_solution_issues, generate_problems, generate_task,
                                generate_front, generate_back, generate_query_response,clean_up_solution, almost_solution_issues)

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



def display_operations(code):
    """
    Display buttons for various operations (documentation, clean code, diagnose issues, etc.) and process them.
    """
    if st.button('Generate Documentation'):
        documentation = generate_documentation(code)
        st.markdown("## Documentation")
        st.code(documentation, language='markdown')
    
    if st.button('Clean Up Code'):
        cleaned_code = generate_clean(code)
        st.markdown("## Cleaned Code")
        st.code(cleaned_code, language='python')
    
    if st.button('Diagnose Code Issues'):
        issues = diagnose_solution_issues(code)
        st.markdown("## Diagnose Issues")
        st.write(issues)

    # Add more operations as needed



def main_ui():
    """
    Main function to render the Streamlit UI components, including Git repository operations.
    """
    #st.set_page_config(page_title="AI Code Assistant", layout="wide")
    st.title("AI Code Assistant")


    # Configuration UI for entering the OpenAI API key
    configuration_expander()   
    # Display a warning if the API key is not set
    if "api_key" not in st.session_state or not st.session_state["api_key"]:
        st.warning("Please enter your Minato key in the Configuration section.")

    st.markdown("""
    Focus on enhancing an existing <span style="color: #2874A6; font-weight: bold;">Codebase</span> 
    by addressing <span style="color: #28B463; font-weight: bold;">Interactive</span> and 
    <span style="color: #CB4335; font-weight: bold;">Practical Real-World</span> Problems.
    """, unsafe_allow_html=True)

    # Clone Git Repository UI
    st.subheader("🌌: Clone Git Repository")
    repo_url = st.text_input("STEP 1: Enter GitHub Repository URL")
    destination = "path/to/clone"  # Adjust the path as needed or make it user input

    if st.button("Clone Repository"):
        message = clone_git_repo(repo_url, destination)
        st.success(message)

    # View Repository Structure UI
    with st.expander("View Repository Structure"):
        if os.path.exists(destination):
            repo_structure = generate_tree_structure(destination)
            st_ace.st_ace(repo_structure, language='text', theme='github', height=300, readonly=True)
        else:
            st.warning("Repository not cloned or path does not exist.")

    # File Selection UI
    st.markdown("""
    <h2>
    <span style="color: #2874A6; font-weight: bold; font-size: 17px;">STEP 2:Please select a file </span>
    </h2>
    """, unsafe_allow_html=True)  
    repo_files = []
    if os.path.exists(destination):
        repo_files = list_files_recursively(destination)
        # Convert absolute paths to relative paths for display
        #repo_files_relative = [os.path.relpath(file, start=destination) for file in repo_files]
        #selected_file = st.selectbox("Select a File to Display", options=repo_files_relative)
        selected_files_paths = st.selectbox("Select a File to Display", repo_files, format_func=lambda x: os.path.relpath(x, destination))


        code_context = ""
        if selected_files_paths:
        
            file_name = os.path.basename(selected_files_paths)
            # Open the selected file
            with open(selected_files_paths, "r") as file:
                # Read the file content


                file_content = file.read()
            file_extension = file_name.split('.')[-1]
            

            
            language_map = {
                'py': 'python', 'js': 'javascript', 'css': 'css',
                'cpp': 'cpp', 'dart': 'dart', 'java': 'java',
                'sol': 'solidity', 'php': 'php', 'cs': 'csharp',
                'go': 'go', 'rb': 'ruby', 'sql': 'sql',
                'swift': 'swift', 'kt': 'kotlin', 'html': 'html',
                'rs': 'rust', 'ts': 'typescript', 'pl': 'perl',
                'lua': 'lua', 'r': 'r', 'mat': 'matlab',
                'hs': 'haskell', 'sh': 'shell', 'ml': 'ocaml',
                'f#': 'fsharp', 'scala': 'scala', 'groovy': 'groovy',
                'vb': 'visualbasic', 'asm': 'assembly', 'elixir': 'elixir',
                'erl': 'erlang', 'prolog': 'prolog', 'lisp': 'lisp',
                'vue': 'vue', 'jsx': 'react', 'tsx': 'react_ts',
                'json': 'json', 'xml': 'xml', 'yaml': 'yaml', 'md': 'markdown'
            }

        
            language = language_map.get(file_extension, 'text')

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
                    index=30)  # Default to 'tomorrow_night_blue'

                # Editor keybinding selection
                keybinding = st.selectbox(
                    'Select Keybinding',
                    ('ace', 'vim', 'emacs', 'sublime', 'vscode', 'textmate'),
                    index=4)  # Default to 'vscode'
                    
            st_ace.st_ace(language=language, value=file_content, keybinding=keybinding, theme=theme, key=f"ace-editor-{file_content}", readonly=True, height=300)

            # Append file content to code_context for further processing
            #code_context += f"\n\nFile Content:\n{file_content}"
            code_context += f"\n\nFile Name: {file_name}\nFile Extension: .{file_extension}\nFile Content:\n{file_content}"



    # Flags to track which button has been pressed
    documentation_clicked = False
    clean_clicked = False
    front_clicked = False
    back_clicked = False

    # Creating a row of columns for the buttons
    col_run, col_diagnose, col_clean , col_back = st.columns(4)

    with col_run:
        documentation_clicked = st.button(' Get Documentation')

    with col_diagnose:
        clean_clicked = st.button("Make this Code Clean")

    with col_clean:
        front_clicked = st.button("Build Front-End")
    
    with col_back:
        back_clicked = st.button("Build Back-End")


    # Display output if 'Almost Solution' button was clicked
    if documentation_clicked:

        
        documentation = generate_documentation(code_context)

        
    # Display diagnosis if 'What's wrong with my solution?' button was clicked
    
    if clean_clicked:
        
        clean = generate_clean(code_context)
        

    # Display cleaned code if 'Make my solution clean' button was clicked
    if front_clicked:

        front = generate_front(code_context)

    # Display cleaned code if 'Make my solution clean' button was clicked
    if back_clicked:
        back = generate_back(code_context)



    #user query section
 
    user_query = st.text_area("", value=st.session_state.get('user_query', ''), 
                              placeholder="Type your question here...", key="query_input", height=100)


    if st.button("🔍", key="query_submit_button"):
        response = generate_query_response(user_query, code_context)
        st.session_state.response = response
            


    # Display the response
    if 'response' in st.session_state and st.session_state.response:
        st.markdown(f"*Minato:*\n{st.session_state.response}")
        
   # with st.expander("Chat History"):

   #     for chat in st.session_state.chat_history:
    #        st.markdown(chat['question'], unsafe_allow_html=True)
    #        st.markdown(chat['answer'], unsafe_allow_html=True)

     #   if st.button("Clear History", key="clear_history_button"):
     #       st.session_state.chat_history = []
            
            
            
            
                    
    # Let make it interactive by Customising Entreprise SOftware
            
    st.markdown("""
            Let's enhance interactivity by implementing <span style="color: #2874A6; font-weight: bold;"> New Features,</span> 
            refining <span style="color: #28B463; font-weight: bold;">Ticketing Functionalities,</span> or
            <span style="color: #CB4335; font-weight: bold;">Removing Unnecessary </span> Elements.
            """, unsafe_allow_html=True)
            

    
    col1, col2 = st.columns(2)

    with col1:


        st.markdown("""
    <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Tasks</span>
    </h2>
    """, unsafe_allow_html=True)

        selected_files_paths = st.selectbox("Select the same File from the Editor on the top", repo_files, format_func=lambda x: os.path.relpath(x, destination))
        task = st.text_area("Describe your task here")

        if st.button("Generate Hints"):
            generate_task(code_context, task)    
    
        # Display the challenge if it's stored in the session state
        if 'task' in st.session_state:
            st.markdown(st.session_state['task'], unsafe_allow_html=True)

            
        # Customise Entreprise SOftware in an expander
        with st.expander("Generate Tasks "):
            difficulty = st.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Hard", "Expert"], key='difficulty')

            selected_files_paths = st.selectbox("Select a File to Work", repo_files, format_func=lambda x: os.path.relpath(x, destination))
        


            if st.button("Generate Related Problems"):
                generate_problems(difficulty, code_context)

            # Display the challenge if it's stored in the session state
            if 'problem' in st.session_state:
                st.markdown(st.session_state['problem'], unsafe_allow_html=True)



    with col2:


        st.markdown("""
    <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Solution Area</span>
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
                index=3)  # Default to 'vscode'
                
            language= st.selectbox(
                'Select Language',
                ('python', 'javascript', 'css',
                'cpp', 'dart', 'java',
                'solidity', 'php', 'csharp',
                'go', 'ruby', 'sql',
                'swift', 'kotlin', 'html',
                'rust', 'typescript', 'perl',
                'lua', 'r', 'matlab',
                'haskell', 'shell', 'ocaml',
                'fsharp', 'scala', 'groovy',
                'visualbasic', 'assembly', 'elixir',
                'erlang', 'prolog', 'lisp'),
                index=0)
                
                
                
        # ACE editor
        code = st_ace.st_ace(language=language, keybinding=keybinding, theme=theme, placeholder="Write your code here...", height=400, key='code')

        solution = code

        st.caption('Click first on  :blue[Apply] before _Run code_  and others :sunglasses:')

        # Flags to track which button has been pressed
        almost_clicked = False
        diagnose_clicked = False
        clean_clicked = False

        # Creating a row of columns for the buttons
        col_run, col_diagnose, col_clean = st.columns(3)

        with col_run:
            almost_clicked = st.button(' Almost There??')

        with col_diagnose:
            diagnose_clicked = st.button("Diagnose Solution")

        with col_clean:
            clean_clicked = st.button("Clean Solution")

        # Display output if 'Almost Solution' button was clicked
        if almost_clicked:

            explanation_output = st.session_state.get('task', '')
            almost = almost_solution_issues(solution, explanation_output, code_context)
            
        # Display diagnosis if 'What's wrong with my solution?' button was clicked
        
        if diagnose_clicked:
            explanation_output = st.session_state.get('task', '')
            diagnosis = diagnose_solution_issues(solution, explanation_output, code_context)
            

        # Display cleaned code if 'Make my solution clean' button was clicked
        if clean_clicked:
            explanation_output = st.session_state.get('task', '')
            cleaned_solution = clean_up_solution(explanation_output, code_context)
            
 



    # Additional information or footer
    st.markdown("---")
    st.markdown("---")

    st.markdown("Developed with :heart: by [Chris NGANDIMOUN](https://www.linkedin.com/in/chris-ngandimoun-745508109?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)")

if __name__ == "__main__":
    main_ui()
