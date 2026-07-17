import os
import requests
import csv
import dotenv
import time
from tabulate import tabulate

# Load environment variables from a .env file
dotenv.load_dotenv()

# Configuration
# Set the GitHub repository to fetch files from
# GITHUB_REPO = input("Enter the GitHub repository (e.g., 'username/repo'): ")
GITHUB_REPO = "Subbarao6338/subbu-apps-practise-coding"
BRANCH_NAME = "main"  # Specify the branch name here
BASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents?ref={BRANCH_NAME}"
# BASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/"
LOCAL_DIR = "local_repo"  # Local directory to save downloaded files
PYTHON_DIR = os.path.join(LOCAL_DIR, "Python")  # Directory for Python files
TEXT_DIR = os.path.join(LOCAL_DIR, "Text")  # Directory for text files

# Set maximum files for each type from environment variables
MAX_PYTHON_FILES = int(os.getenv("MAX_PYTHON_FILES"))
MAX_TEXT_FILES = int(os.getenv("MAX_TEXT_FILES"))

# Get GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if GITHUB_TOKEN is None:
    raise ValueError("GitHub token is not set. Please set the GITHUB_TOKEN environment variable.")

# Create local directories for storing downloaded files
os.makedirs(PYTHON_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

# List to store metadata about downloaded files
metadata = []

def fetch_files(url):
    """Fetch files from the given GitHub API URL."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()  # Return the JSON response


def get_file_metadata(file_path):
    """Get the latest commit metadata for a given file path from the GitHub repository."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    commits_url = f"https://api.github.com/repos/{GITHUB_REPO}/commits?path={file_path}&per_page=1"
    response = requests.get(commits_url, headers=headers)
    response.raise_for_status()
    commits = response.json()

    # Check if there are commits and return the creation date and message
    if commits:
        creation_date = commits[0]['commit']['committer']['date']
        commit_message = commits[0]['commit']['message'] if commits[0]['commit']['message'] else 'No commit message'
        return (creation_date, commit_message)
    else:
        return ('N/A', 'No commits available')

def download_file(file_url, save_dir, file_name, github_path):
    """Download a file from the given URL and save it to the specified directory."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    file_response = requests.get(file_url, headers=headers)
    file_response.raise_for_status()

    # Handle duplicate filenames by appending a counter
    new_file_name = file_name
    counter = 1
    while os.path.exists(os.path.join(save_dir, new_file_name)):
        base_name, extension = os.path.splitext(file_name)
        new_file_name = f"{base_name}_{counter}{extension}"
        counter += 1

    # Save the file content to the local directory
    with open(os.path.join(save_dir, new_file_name), 'wb') as f:
        f.write(file_response.content)

    # Get metadata for the downloaded file using the GitHub path
    creation_date, commit_message = get_file_metadata(github_path)
    metadata.append({
        'File Location': os.path.join(save_dir, new_file_name),
        'File URL': file_url,
        'Creation Date': creation_date,
        'Size (bytes)': len(file_response.content),
        'Commit Message': commit_message
    })

def process_directory(url):
    """Recursively process the directory at the given URL to download files."""
    items = fetch_files(url)  # Fetch items in the current directory
    for item in items:
        if item['type'] == 'file':
            # Check file type and download if within limits
            if item['name'].endswith('.py') and len([m for m in metadata if m['File Location'].endswith('.py')]) < MAX_PYTHON_FILES:
                download_file(item['download_url'], PYTHON_DIR, item['name'], item['path'])
            elif item['name'].endswith(('.txt', '.md')) and len([m for m in metadata if m['File Location'].endswith(('.txt', '.md'))]) < MAX_TEXT_FILES:
                download_file(item['download_url'], TEXT_DIR, item['name'], item['path'])
        elif item['type'] == 'dir':
            # Recursively process subdirectories
            process_directory(f"https://api.github.com/repos/{GITHUB_REPO}/contents/{item['path']}?ref={BRANCH_NAME}")


def main():
    """Main function to orchestrate the downloading of files and saving metadata."""
    print("Starting the download process... Please wait.")
    start_time = time.time()  # Record the start time
    process_directory(BASE_URL)  # Start processing the base directory

    # Write metadata to a CSV file
    csv_file_path = os.path.join(LOCAL_DIR, 'file_metadata.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metadata[0].keys())
        writer.writeheader()
        writer.writerows(metadata)

    # Print completion message with processing time
    print(f"Process completed. Metadata saved to {csv_file_path}.")
    print(f"Total processing time: {time.time() - start_time:.2f} seconds.")

    # Display the contents of the metadata in a tabular format
    print("\nFile Metadata:")
    print(tabulate(metadata, headers="keys", tablefmt="simple"))

if __name__ == "__main__":
    main()
