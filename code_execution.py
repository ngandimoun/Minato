import io
import sys
import contextlib
from contextlib import redirect_stdout, redirect_stderr
import importlib

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
