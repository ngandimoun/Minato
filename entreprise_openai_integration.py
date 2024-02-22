#open ai config for entreprise_software.py


import openai
import os
import streamlit as st

# Initialize the OpenAI client with API key

def get_openai_client():
    """
    Initializes and returns the OpenAI client using the API key provided by the user.
    The API key is expected to be stored in the Streamlit session state.
    
    Returns:
        openai.Client: The initialized OpenAI client if the API key is available.
        None: If the API key is not set or missing.
    """
    #api_key = st.session_state.get("api_key")
    api_key = os.getenv('OPENAI_API_KEY') or st.session_state.get("api_key")
    
    if api_key:
        openai.api_key = api_key
        return openai
    else:
        st.error("OpenAI API key is not set. Please enter your API key in the configuration.")
        return None


# Function to generate a clean solution
def clean_up_solution(explanation_output, code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not explanation_output:
        return "Solution or question statement is missing."
        
    # Determine the language from the code context or user query
    language = determine_language(code_context)
    combined_prompt = f"Based of this {code_context} , and {explanation_output}\n\nGive a solution code:"

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```language\n{stream_response.choices[0].text.strip()}\n```"

        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"


# Function to diagnose issues in the user code
def diagnose_solution_issues(solution, explanation_output, code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato key provided.")
        return "Error: No Minato  key."

    if not solution or not explanation_output:
        return "Solution or Question statement is missing."

    combined_prompt = f"Based of this {code_context}, and {explanation_output}\n\nSolution:\n{solution}\n\nDiagnose any issues present in the solution and provide explanations for them:"

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = stream_response.choices[0].text.strip()
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"



# Function to give almost solution of the users code
def almost_solution_issues(solution, explanation_output, code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not solution or not explanation_output:
        return "Solution or question statement or selected_files_paths  is missing."

    combined_prompt = f"Based of this: {code_context} ,  and: {explanation_output}\n\nSolution:\n{solution}\n\nEvaluate the solution to determine if it is nearly correct. Provide guidance on what steps to take next :"

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = stream_response.choices[0].text.strip()
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"
        
        

# Define the function to generate a Task based of codebase file
def generate_problems(difficulty, code_context):
    full_response = ""
    message_placeholder = st.empty()

    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return

    combined_prompt = f"Create a {difficulty} level computer science task related to {code_context}, Please suggest a practical task for modifying an existing functionality or adding a new one. " \
                      f"Provide a problem statement."

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
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


        colored_response = f"""
            <p><span style='color: red;'>{problem_statement_label}:</span>{problem_statement_content}</p> <!-- Problem Statement -->

        """
            

        # Store the colored response directly in the session state
        st.session_state['problem'] = colored_response

    except Exception as e:
        st.error(f"An error occurred: {e}")   


#generate solution from given task with codebase file

def generate_task(code_context, task):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not task:
        return "task statement is missing."

   
    combined_prompt = f"Based of this {code_context} Read carefully the Question: {task}\n\nProvide a explanation output, hint1, and hint2."
    

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.5,
            max_tokens=350,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )


        full_response = stream_response.choices[0].text.strip()


        sections = full_response.split('\n\n')

        # Separate labels and contents for each section
        explanation_output_label, explanation_output_content = sections[0].split(':', 1)
        hint1_input_label, hint1_input_content = sections[1].split(':', 1)
        hint2_output_label, hint2_output_content = sections[2].split(':', 1)

        colored_response = f"""
            <p><span style='color: red;'>{explanation_output_label}:</span>{explanation_output_content}</p> <!-- Explanation Output -->
            <p><span style='color: blue;'>{hint1_input_label}:</span>{hint1_input_content}</p> <!-- Hint1 Input -->
            <p><span style='color: green;'>{hint2_output_label}:</span>{hint2_output_content}</p> <!-- Hint2 Output -->
        """ 

        # Store the colored response directly in the session state
        st.session_state['task'] = colored_response

    except Exception as e:
        st.error(f"An error occurred: {e}") 

# Function to add documentation to the provided code
def generate_documentation(code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not code_context:
        return "Selected file is missing."
        


  
    user_query = f"Give a documentation."

    
    
    combined_prompt = (
        f"Read carefully the code:\n{code_context}\n\n"
        f"Enhancement request: {user_query}\n\n"
        "Answer:"
    )

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = stream_response.choices[0].text.strip()
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"




# Function to give clean code to the provided code
def generate_clean(code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not code_context:
        return "Selected file is missing."
        
    # Determine the language from the code context or user query
    language = determine_language(code_context)

    user_query = "Please improve this code by ensuring it is clean and efficient. Identify and automatically correct any instances of dead or duplicate code, code smells, overly complex structures, and security vulnerabilities. Additionally, please provide comments explaining each change you make for clarity and understanding."
    
    combined_prompt = (
        f"Read carefully the code:\n{code_context}\n\n"
        f"Enhancement request: {user_query}\n\n"
        "Answer:"
    )

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        #full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        full_response = f"```language\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"


# Function to generate front end code to the provided code
def generate_front(code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not code_context:
        return "Selected file is missing."
        
    # Determine the language from the code context or user query
    language = determine_language(code_context)
    user_query = "Please examine the provided code and determine if it is suitable for a frontend implementation. If it is, kindly generate the corresponding frontend code. However, if a frontend component is not applicable or necessary for this code, please indicate that no frontend development is required."
    
    combined_prompt = (
        f"Read carefully the code:\n{code_context}\n\n"
        f"Enhancement request: {user_query}\n\n"
        "Answer:"
    )

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.3,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )



        #full_response = stream_response.choices[0].text.strip()
        full_response = f"```language\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"
        

# Function to generate back end code to the provided code
def generate_back(code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not code_context:
        return "Selected file is missing."
        
    # Determine the language from the code context or user query
    language = determine_language(code_context)

    user_query = "Please examine the provided code and determine if it is suitable for a backend implementation. If it is, kindly generate the corresponding backend code. However, if a backend component is not applicable or necessary for this code, please indicate that no backend development is required."
    
    combined_prompt = (
        f"Read carefully the code:\n{code_context}\n\n"
        f"Enhancement request: {user_query}\n\n"
        "Answer:"
    )

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.4,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        #full_response = stream_response.choices[0].text.strip()
        full_response = f"```language\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"




def generate_query_response(user_query, code_context):
    try:
    
        client = get_openai_client()
        if client is None:
            return "No Minato Key provided."
        # Determine the language from the code context or user query
        language = determine_language(code_context)

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
        #formatted_response = format_response(response.choices[0].text.strip(), language)
        
        full_response = f"```language\n{response.choices[0].text.strip()}\n```"
        

        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"



def determine_language(code_context):
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
        'swift': 'swift', 'kt': 'kotlin', 'html': 'html',
        'rs': 'rust', 'ts': 'typescript', 'pl': 'perl',
        'lua': 'lua', 'r': 'r', 'mat': 'matlab',
        'hs': 'haskell', 'sh': 'shell', 'ml': 'ocaml',
        'f#': 'fsharp', 'scala': 'scala', 'groovy': 'groovy',
        'vb': 'visualbasic', 'asm': 'assembly', 'elixir': 'elixir',
        'erl': 'erlang', 'prolog': 'prolog', 'lisp': 'lisp'
    }

    # Logic to determine the language from code_context or user_query
    # This is a placeholder, and you might need a more sophisticated method
    for key, value in language_map.items():
        if key in code_context:
            return value

    # Default to 'text' if no specific language is identified
    return 'text'
