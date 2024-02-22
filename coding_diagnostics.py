import os
import openai
import streamlit as st


# Assuming get_openai_client is defined in openai_utils.py or similar
from coding_openai_utils import get_openai_client



# Function to diagnose issues in the user's Python code
def diagnose_code_issues(code, problem_statement, sample_input):
    client = get_openai_client()
    if client is None:
        return "Error: OpenAI client could not be initialized."

    if not code or not problem_statement:
        return "Code or problem statement is missing."

    model = "gpt-3.5-turbo-instruct"  # Specify the appropriate model for code diagnostics
    combined_prompt = f"Problem Statement: {problem_statement}\nSample Input: {sample_input}\nPython Code:\n{code}\n\nDiagnose any issues with the code and explain them:"

    try:
        response = client.completions.create(
            model=model,
            prompt=combined_prompt,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"An error occurred while diagnosing the code: {e}")
        return f"Error: {e}"

# Function to suggest cleaner code solutions
def clean_up_code(problem_statement, sample_input):
    client = get_openai_client()
    if client is None:
        return "Error: OpenAI client could not be initialized."

    if not problem_statement:
        return "Problem statement is missing."

    model = "gpt-3.5-turbo-instruct"  # Specify the appropriate model for code cleanup
    combined_prompt = f"Problem Statement: {problem_statement}\nSample Input: {sample_input}\nProvide a clean, optimized Python code solution:"

    try:
        response = client.completions.create(
            model=model,
            prompt=combined_prompt,
            temperature=0.7,
            max_tokens=250,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        clean_code_solution = f"```python\n{response.choices[0].text.strip()}\n```"
        return clean_code_solution
    except Exception as e:
        st.error(f"An error occurred while cleaning up the code: {e}")
        return f"Error: {e}"
