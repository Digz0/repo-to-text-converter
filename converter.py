import os
from git import Repo
import tempfile
import mimetypes
import chardet

def clone_repo(repo_url, local_path):
    Repo.clone_from(repo_url, local_path)

def is_text_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and (mime_type.startswith('text/') or mime_type in ['application/json', 'application/xml']):
        return True
    try:
        with open(file_path, 'rb') as file:
            return b'\0' not in file.read(1024) and chardet.detect(file.read(1024))['encoding'] is not None
    except IOError:
        return False

def repo_to_text(repo_url, output_file):
    with tempfile.TemporaryDirectory(prefix="repo_") as temp_dir:
        try:
            clone_repo(repo_url, temp_dir)
            all_text = []
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if is_text_file(file_path):
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        all_text.append(f"File: {file_path}\n\n{content}\n\n")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(all_text))
        except Exception as e:
            print(f"An error occurred: {e}")

# Usage
repo_url = "https://github.com/Digz0/RevisarAI"
output_file = "temp_repo_content.txt"
repo_to_text(repo_url, output_file)