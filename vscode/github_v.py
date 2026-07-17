import os
import requests
import csv
import dotenv
import time
from tabulate import tabulate

# Load environment variables from a .env file
dotenv.load_dotenv("./Config/.env")

# Configuration
LOCAL_DIR = "local_repo"  # Local directory to save downloaded files
PYTHON_DIR = os.path.join(LOCAL_DIR, "Python")  # Directory for Python files
TEXT_DIR = os.path.join(LOCAL_DIR, "Text")  # Directory for text files

# Set maximum files for each type from environment variables or default to 5
MAX_PYTHON_FILES = int(os.getenv("MAX_PYTHON_FILES", 5))
MAX_TEXT_FILES = int(os.getenv("MAX_TEXT_FILES", 5))

# Get GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if GITHUB_TOKEN is None:
    raise ValueError("GitHub token is not set. Please set the GITHUB_TOKEN environment variable.")

# Create local directories for storing downloaded files
os.makedirs(PYTHON_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

# List to store metadata about downloaded and skipped files
metadata = []
downloaded_urls = set()  # Set to keep track of downloaded file URLs

# GitHub repository and branch variables
GITHUB_REPO = "Subbarao6338/subbu-apps-practise-coding"
BRANCH_NAME = "main"  # Default branch

def fetch_branches():
    """Fetch branches from the GitHub repository."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    branches_url = f"https://api.github.com/repos/{GITHUB_REPO}/branches"
    try:
        response = requests.get(branches_url, headers=headers)
        response.raise_for_status()
        return [branch['name'] for branch in response.json()]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def fetch_files(url):
    """Fetch files from the given GitHub API URL."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_file_metadata(file_path):
    """Get the latest commit metadata for a given file path from the GitHub repository."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    commits_url = f"https://api.github.com/repos/{GITHUB_REPO}/commits?path={file_path}&per_page=1&ref={BRANCH_NAME}"
    response = requests.get(commits_url, headers=headers)
    response.raise_for_status()
    commits = response.json()

    if commits:
        creation_date = commits[0]['commit']['committer']['date']
        commit_message = commits[0]['commit']['message'] or 'No commit message'
        return (creation_date, commit_message)
    else:
        return ('N/A', 'This file has no commit history.')

def normalize_url(url):
    """Normalize the URL by removing trailing slashes."""
    return url.rstrip('/')

import hashlib

def calculate_checksum(file_path):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def download_file(file_url, save_dir, file_name, github_path):
    """Download a file from the given URL and save it to the specified directory."""
    normalized_url = normalize_url(file_url)
    base_name, extension = os.path.splitext(file_name)
    new_file_name = f"{BRANCH_NAME}_{base_name}{extension}"
    local_file_path = os.path.join(save_dir, new_file_name)

    # Get the latest commit metadata for the file
    creation_date, commit_message = get_file_metadata(github_path)

    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    file_response = requests.get(file_url, headers=headers)
    file_response.raise_for_status()

    # Check if the file has been modified since the last download
    if os.path.exists(local_file_path):
        local_file_size = os.path.getsize(local_file_path)
        local_checksum = calculate_checksum(local_file_path)
        remote_checksum = hashlib.md5(file_response.content).hexdigest()

        # Check if the file size and checksum match
        if local_file_size == len(file_response.content) and local_checksum == remote_checksum:
            print(f"Skipping {local_file_path} as it is up-to-date.")
            metadata.append({
                'File Location': local_file_path,
                'File URL': normalized_url,
                'Creation Date': creation_date,
                'Size (bytes)': local_file_size,
                'Commit Message': commit_message,
                'Status': 'Skipped'
            })
            return  # Skip downloading this file

    # Proceed to download if the file does not exist or has been modified
    with open(local_file_path, 'wb') as f:
        f.write(file_response.content)
    print(f"File {local_file_path} downloaded successfully.")
    metadata.append({
        'File Location': local_file_path,
        'File URL': normalized_url,
        'Creation Date': creation_date,
        'Size (bytes)': len(file_response.content),
        'Commit Message': commit_message,
        'Status': 'Downloaded'
    })
    downloaded_urls.add(normalized_url)


def handle_file_download(item):
    """Handle the downloading of a file based on its type."""
    if item['name'].endswith('.py') and len(
            [m for m in metadata if m['File Location'].endswith('.py')]) < MAX_PYTHON_FILES:
        download_file(item['download_url'], PYTHON_DIR, item['name'], item['path'])  # Pass github_path
    elif item['name'].endswith(('.txt', '.md')) and len(
            [m for m in metadata if m['File Location'].endswith(('.txt', '.md'))]) < MAX_TEXT_FILES:
        download_file(item['download_url'], TEXT_DIR, item['name'], item['path'])  # Pass github_path

def process_directory(url):
    """Recursively process the directory at the given URL to download files."""
    items = fetch_files(url)
    for item in items:
        if item['type'] == 'file':
            handle_file_download(item)
        elif item['type'] == 'dir':
            process_directory(f"https://api.github.com/repos/{GITHUB_REPO}/contents/{item['path']}?ref={BRANCH_NAME}")

def save_metadata_to_csv():
    """Save the collected metadata to a CSV file."""
    csv_file_path = os.path.join(LOCAL_DIR, 'file_metadata.csv')
    if metadata:
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=metadata[0].keys())
            writer.writeheader()
            writer.writerows(metadata)
    else:
        print("No metadata to save.")
    return csv_file_path

def display_metadata():
    """Display the contents of the metadata in a tabular format."""
    if metadata:
        print("\nFile Metadata:")
        print(tabulate(metadata, headers="keys", tablefmt="simple"))
    else:
        print("No metadata to display.")

def main():
    """Main function to orchestrate the downloading of files and saving metadata."""
    global BRANCH_NAME  # Declare global variable for branch name

    print("Fetching branches from the repository...")
    branches = fetch_branches()

    # Display branches and prompt user for branch selection
    print("Available branches:")
    for idx, branch in enumerate(branches):
        print(f"{idx + 1}: {branch}")

    # Prompt user for branch selection
    while True:
        branch_choice = input(f"Select a branch (default is 'main', enter number or branch name): ")
        if branch_choice.isdigit() and 1 <= int(branch_choice) <= len(branches):
            BRANCH_NAME = branches[int(branch_choice) - 1]
            break
        elif branch_choice == "":
            BRANCH_NAME = "main"
            break
        else:
            print("Invalid choice. Please try again.")

    print(f"Using branch: {BRANCH_NAME}")

    # Update BASE_URL with the selected branch
    global BASE_URL
    BASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents?ref={BRANCH_NAME}"

    print("Starting the download process... Please wait.")
    start_time = time.time()  # Record the start time
    process_directory(BASE_URL)  # Start processing the base directory

    # Save metadata to a CSV file
    csv_file_path = save_metadata_to_csv()

    # Print completion message with processing time
    print(f"Process completed. Metadata saved to {csv_file_path}.")
    print(f"Total processing time: {time.time() - start_time:.2f} seconds.")

    # Display the metadata
    display_metadata()

if __name__ == "__main__":
    main()
