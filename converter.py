import os
import sys
from git import Repo
import tempfile
import mimetypes
import chardet
from tqdm import tqdm

def clone_repo(repo_url, local_path):
    Repo.clone_from(repo_url, local_path)

def is_text_file(file_path):
    # Add Dockerfile to the list of explicitly recognized text files
    if os.path.basename(file_path).lower() == 'dockerfile':
        return True
    
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
            print("Cloning repository...")
            clone_repo(repo_url, temp_dir)
            all_text = []
            total_files = sum([len(files) for _, _, files in os.walk(temp_dir)])
            
            with tqdm(total=total_files, desc="Processing files") as pbar:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if is_text_file(file_path):
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            all_text.append(f"File: {file_path}\n\n{content}\n\n")
                        pbar.update(1)
            
            print("Writing output file...")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(all_text))
            print(f"Repository content saved to {output_file}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python converter.py <repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    output_file = "temp_repo_content.txt"
    repo_to_text(repo_url, output_file)
