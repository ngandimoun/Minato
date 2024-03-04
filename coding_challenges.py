import os
import openai
import streamlit as st

# Assuming get_openai_client is defined in openai_utils.py or similar
from coding_openai_utils import get_openai_client

def generate_python_challenge(difficulty, topic):
    """
    Generates a Python programming challenge based on the specified difficulty and topic.
    
    Parameters:
    - difficulty (str): The difficulty level of the challenge (e.g., "Easy", "Medium").
    - topic (str): The topic for the challenge (e.g., "Data Structures", "Algorithms").
    
    Returns:
    - str: A formatted string containing the challenge.
    """
    client = get_openai_client()
    if client is None:
        st.error("OpenAI client could not be initialized due to missing API key.")
        return

    model = "gpt-3.5-turbo-instruct"  # Or the latest appropriate model for generating coding challenges
    #prompt = f"Create a Python3 programming challenge of {difficulty} difficulty level related to {topic}. Include a problem statement, sample input, expected output, and a hint."
    prompt = f"Create a {difficulty} level Python3 challenge related to {topic}. " \
                      f"Provide a problem statement, sample input, expected output, explanation and hint."

    try:
        response = client.completions.create(
            model=model,
            prompt=prompt,
            temperature=0.5,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )


    
        full_response = response.choices[0].text.strip()


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




