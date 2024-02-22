#git operation config for entreprise_software.py

import git
import os
from entreprise_file_management import clear_directory

def clone_git_repo(repo_url, destination):
    """
    Clones a Git repository to a specified destination directory.

    Parameters:
    - repo_url: URL of the Git repository to clone.
    - destination: Local directory path to clone the repository into.

    Returns:
    A string message indicating the result of the clone operation.
    """
    try:
        # Clear the destination directory before cloning
        clear_directory(destination)
        
        # Clone the repository using GitPython
        git.Repo.clone_from(repo_url, destination)
        return f"Repository cloned successfully to {destination}."
    except Exception as e:
        return f"Error cloning repository: {e}"


