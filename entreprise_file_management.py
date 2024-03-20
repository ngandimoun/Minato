#file management config for entreprise_software.py

import os
import shutil
import stat
import time

def on_rm_error(func, path, exc_info):
    """
    Callback function to remove read-only attributes from a file and retry its removal.
    
    Parameters:
    - func: The function that raised the exception.
    - path: Path to the file causing the error.
    - exc_info: Exception information returned by sys.exc_info().
    """
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

def clear_directory(directory):
    """
    Clears all contents of a specified directory, creating it if it doesn't exist.

    Parameters:
    - directory: The path to the directory to clear.
    """
    if os.path.exists(directory):
        for _ in range(5):  # Retry loop in case of locking issues
            try:
                shutil.rmtree(directory, onerror=on_rm_error)
                os.makedirs(directory)
                return
            except Exception as e:
                print(f"Attempt to clear directory failed: {e}")
                time.sleep(1)  # Wait for any locks to be released
    else:
        os.makedirs(directory)  # Create the directory if it doesn't exist

    raise Exception(f"Unable to clear the directory: {directory}")



#function to give all the repo contents  
def generate_tree_structure(startpath):
    """
    Generates a tree structure of directories and files starting from a given path.

    Parameters:
    - startpath: The root directory path to generate the tree structure from.

    Returns:
    A string representing the tree structure of directories and files.
    """
      
    tree = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree.append('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree.append('{}{}'.format(subindent, f))
    return "\n".join(tree)



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
    
def list_files_recursively(directory):
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if not is_image_or_video(file):
                all_files.append(os.path.join(root, file))
    return all_files

 #function to exclude unnecessary files such as videos, images and others
def is_image_or_video(file_name):
    # Define a list of common image and video file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.otf', '.svg', '.txt', '.rst', '.log', '.cfg', '.conf', '.ini', '.csv']
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.rev', '.less', '.scss', '.sass', '.eps', '.ai', '.psd', '.pack', '.webm', '.webp',  '.svgz', '.ttf', '.woff', '.woff2', '.eot', '.mkv']


    # Check if the file has an image or video extension
    file_extension = os.path.splitext(file_name)[1].lower()
    return file_extension in image_extensions or file_extension in video_extensions
