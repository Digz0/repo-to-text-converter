import os  # Import for file and directory operations
import sys  # Import for accessing command-line arguments
from git import Repo  # Import for Git repository operations
import tempfile  # Import for creating temporary directories
from tqdm import tqdm  # Import for progress bar functionality

def clone_repo(repo_url, local_path):
    Repo.clone_from(repo_url, local_path)  # Clone the repository to the specified local path

def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read(1024)
        return True
    except UnicodeDecodeError:
        return False

def repo_to_text(repo_url, output_file):
    with tempfile.TemporaryDirectory(prefix="repo_") as temp_dir:  # Create a temporary directory
        try:
            print("Cloning repository...")  # Print status message
            clone_repo(repo_url, temp_dir)  # Clone the repository
            all_text = []  # Initialize list to store file contents
            total_files = sum([len(files) for _, _, files in os.walk(temp_dir)])  # Count total files in the repo
            
            with tqdm(total=total_files, desc="Processing files") as pbar:  # Create progress bar
                for root, _, files in os.walk(temp_dir):  # Walk through all directories and files
                    for file in files:  # Iterate through each file
                        file_path = os.path.join(root, file)  # Get the full file path
                        if is_text_file(file_path):  # Check if it's a text file
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:  # Open the file
                                content = f.read()  # Read the file content
                            all_text.append(f"File: {file_path}\n\n{content}\n\n")  # Add file path and content to the list
                        pbar.update(1)  # Update the progress bar
            
            print("Writing output file...")  # Print status message
            with open(output_file, 'w', encoding='utf-8') as f:  # Open the output file
                f.write("\n".join(all_text))  # Write all text content to the file
            print(f"Repository content saved to {output_file}")  # Print completion message
        except Exception as e:
            print(f"An error occurred: {e}")  # Print error message if an exception occurs

if __name__ == "__main__":
    if len(sys.argv) != 2:  # Check if the correct number of arguments is provided
        print("Usage: python converter.py <repo_url>")  # Print usage instructions
        sys.exit(1)  # Exit the script with an error code

    repo_url = sys.argv[1]  # Get the repository URL from command-line argument
    output_file = "temp_repo_content.txt"  # Set the output file name
    repo_to_text(repo_url, output_file)  # Call the main function to process the repository
