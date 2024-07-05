# repo-to-text-converter

This Python script clones a GitHub repository and extracts the content of text files into a single output file.

## Usage

Run the script from the command line, providing the GitHub repository URL as an argument:

py converter.py <repo_url>

## Requirements

- Python 3.x
- GitPython
- chardet
- tqdm

To install the required packages, use pip with the provided requirements.txt file:

py -m pip install -r requirements.txt

## Features

- Clones a specified GitHub repository
- Identifies and processes text files within the repository
- Combines content from all text files into a single output file
- Handles various text encodings
- Displays a progress bar during file processing

## Output

The script generates a file named "temp_repo_content.txt" containing the extracted text content from the repository.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.

## License

This project is licensed under the MIT License - see the LICENSE file for details.