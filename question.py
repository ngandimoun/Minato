import streamlit as st
import openai

import streamlit_ace as st_ace
import contextlib
import io
import sys
from openai import OpenAI


# Define the function to get the OpenAI client
def get_openai_client():
    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key

    openai.api_key = os.getenv('OPENAI_API_KEY')
    return openai


# Function to execute the Python code safely
def execute_python_code(code):
    output = io.StringIO()  # Create a string buffer to capture the outputs
    try:
        # Redirect standard output and standard error to the buffer
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            exec(code)  # Execute the code
    except Exception as e:
        output.write(f'Error: {e}')  # Capture errors in the output buffer

    return output.getvalue()  # Return the contents of the buffer




# Function to diagnose issues in the code
def diagnose_solution_issues(solution, question_statement):
    client = get_openai_client()
    if client is None:
        st.error("No OpenAI API key provided.")
        return "Error: No OpenAI API key."

    if not solution or not question_statement:
        return "Solution or Question statement is missing."

    combined_prompt = f"Question Statement: {question_statement}\n\nSolution:\n{solution}\n\nDiagnose any issues present in the solution and provide explanations for them:"

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

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"



# Function generate hint of questions
def generate_hint(question):
    client = get_openai_client()
    if client is None:
        st.error("No OpenAI API key provided.")
        return "Error: No OpenAI API key."

    if not question:
        return "Question statement is missing."

   
    combined_prompt = f"Read carefully the Question: {question}\n\nProvide a explanation output, hint1, and hint2."
   
    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.5,
            max_tokens=150,
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
        st.session_state['question'] = colored_response

    except Exception as e:
        st.error(f"An error occurred: {e}") 
        

# Function to clean up the code
def clean_up_solution(solution, question_statement):
    client = get_openai_client()
    if client is None:
        st.error("No OpenAI API key provided.")
        return "Error: No OpenAI API key."

    if not solution or not question_statement:
        return "Solution or question statement is missing."

    combined_prompt = f"Question Statement: {question_statement}\n\nSolution:\n{solution}\n\nRefactor the solution to enhance its cleanliness and efficiency:"

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

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"

# Function to give almost solution
def almost_solution_issues(solution, question_statement):
    client = get_openai_client()
    if client is None:
        st.error("No OpenAI API key provided.")
        return "Error: No OpenAI API key."

    if not solution or not question_statement:
        return "Solution or question statement is missing."

    combined_prompt = f"Question Statement: {question_statement}\n\nSolution:\n{solution}\n\nEvaluate the solution to determine if it is nearly correct. Provide guidance on what steps to take next :"

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

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"

# Define the function to generate a Python challenge
def generate_problems(difficulty, topic):
    full_response = ""
    message_placeholder = st.empty()

    client = get_openai_client()
    if client is None:
        st.error("No OpenAI API key provided.")
        return

    combined_prompt = f"Create a {difficulty} level computer science related to {topic}. " \
                      f"Provide a problem statement."

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


# Main function for the Streamlit app
def main():
    #st.set_page_config(layout="wide")


    col1, col2 = st.columns(2)

    with col1:


        st.markdown("""
        <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Problems</span>
        </h2>
        """, unsafe_allow_html=True)
        
        question = st.text_area("Write your Problem here")

        if st.button("Generate Hints"):
            generate_hint(question)    
    
        # Display the challenge if it's stored in the session state
        if 'question' in st.session_state:
            st.markdown(st.session_state['question'], unsafe_allow_html=True)

            
        # Computer Science Problems in an expander
        with st.expander("Computer Science Problems"):
            difficulty = st.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Hard", "Expert"], key='difficulty')

            # Expanded list of topics
            topics = [
                "Math", "Algorithm", "Array", "Binary Search", 
                "Dynamic Programming", "Graph Theory", "Data Structures", 
                "String Manipulation", "Recursion", "Sorting Algorithms", 
                "Machine Learning Basics", "Networking", "Database Management", 
                "Operating Systems", "Object-Oriented Programming", 
                "Functional Programming", "Web Development", "Mobile App Development",
                "Security and Cryptography", "Cloud Computing", "Artificial Intelligence",
                "Game Development", "Quantum Computing", "Big Data Analysis"
            ]
            topic = st.selectbox("Select Topic", topics, key='topic')


            if st.button("Generate Computer Science Problem"):
                generate_problems(difficulty, topic)

            # Display the challenge if it's stored in the session state
            if 'problem' in st.session_state:
                st.markdown(st.session_state['problem'], unsafe_allow_html=True)



    with col2:

        st.markdown("""
        <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Solution Area</span>
        </h2>
        """, unsafe_allow_html=True)
        
        solution = st.text_area("Write your solution here")
        


        # Flags to track which button has been pressed
        almost_clicked = False
        diagnose_clicked = False
        clean_clicked = False

        # Creating a row of columns for the buttons
        col_run, col_diagnose, col_clean = st.columns(3)

        with col_run:
            almost_clicked = st.button(' Almost There??')

        with col_diagnose:
            diagnose_clicked = st.button("Solution Checking")

        with col_clean:
            clean_clicked = st.button("Clean Solution")

        # Display output if 'Almost Solution' button was clicked
        if almost_clicked:

            question_statement = st.session_state.get('question', '')
            almost = almost_solution_issues(solution, question_statement)
            
        # Display diagnosis if 'What's wrong with my solution?' button was clicked
        
        if diagnose_clicked:
            question_statement = st.session_state.get('question', '')
            diagnosis = diagnose_solution_issues(solution, question_statement)
            

        # Display cleaned code if 'Make my solution clean' button was clicked
        if clean_clicked:
            question_statement = st.session_state.get('question', '')
            cleaned_solution = clean_up_solution(solution, question_statement)
            



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