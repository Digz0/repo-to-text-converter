import os
import re
from git import Repo
import time
import shutil
from git.exc import GitCommandError
import tempfile
import mimetypes
import chardet

def clone_repo(repo_url, local_path):
    Repo.clone_from(repo_url, local_path)

def get_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""

def preprocess_text(text):
    # Remove comments (for programming languages)
    text = re.sub(r'\/\/.*|\/\*[\s\S]*?\*\/', '', text)
    # Remove trailing whitespace from each line
    text = '\n'.join(line.rstrip() for line in text.splitlines())
    return text

def is_text_file(file_path):
    # Initialize mimetypes
    mimetypes.init()

    # Get the MIME type of the file
    mime_type, _ = mimetypes.guess_type(file_path)

    # Check if it's a known text MIME type
    if mime_type and (mime_type.startswith('text/') or mime_type in ['application/json', 'application/xml']):
        return True

    # If MIME type is not recognized or not text, try to detect encoding
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read(1024)  # Read first 1024 bytes
            if not raw_data:
                return False  # Empty file
            if b'\0' in raw_data:
                return False  # Binary file
            result = chardet.detect(raw_data)
            if result['encoding'] is not None:
                return True  # Likely a text file if we can detect an encoding
    except IOError:
        return False

    return False  # If all else fails, assume it's not a text file

def repo_to_text(repo_url, output_file):
    with tempfile.TemporaryDirectory(prefix="repo_") as temp_dir:
        try:
            # Clone the repository
            clone_repo(repo_url, temp_dir) 
            
            all_text = []
            
            # Walk through the repository
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if is_text_file(file_path):
                        content = get_file_content(file_path)
                        processed_content = preprocess_text(content)
                        all_text.append(f"File: {file_path}\n\n{processed_content}\n\n")
            
            # Combine all processed text
            final_text = "\n".join(all_text)
            
            # Write to output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_text)
                
        except Exception as e:
            print(f"An error occurred: {e}")

# Usage
repo_url = "https://github.com/Digz0/RevisarAI"
output_file = "temp_repo_content.txt"
repo_to_text(repo_url, output_file)
