import os
import requests
import csv
import time
import dotenv  # To load environment variables from a .env file
import threading  # For running the spinner in a separate thread
import sys  # For flushing output

# Load environment variables from .env file
dotenv.load_dotenv()

# Configuration
GITHUB_REPO = "microsoft/autogen"  # GitHub repository
BASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/"
LOCAL_PYTHON_DIR = "Python"
LOCAL_TEXT_DIR = "Text"
CSV_FILE = "file_metadata.csv"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Get token from environment variable

# Check if GITHUB_TOKEN is set
if GITHUB_TOKEN is None:
    raise ValueError("GITHUB_TOKEN environment variable is not set.")

# Create local directories if they don't exist
os.makedirs(LOCAL_PYTHON_DIR, exist_ok=True)
os.makedirs(LOCAL_TEXT_DIR, exist_ok=True)

# Function to check rate limit
def check_rate_limit():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get("https://api.github.com/rate_limit", headers=headers)
    if response.status_code == 200:
        rate_limit_info = response.json()
        remaining = rate_limit_info['rate']['remaining']
        reset_time = rate_limit_info['rate']['reset']
        return remaining, reset_time
    return None, None

# Function to fetch files from GitHub repository
def fetch_files(url):
    while True:
        remaining, reset_time = check_rate_limit()
        if remaining is not None and remaining == 0:
            wait_time = reset_time - int(time.time()) + 5  # Wait until the rate limit resets
            print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            break

    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch files: {response.status_code} - {response.text}")
        return []

# Function to download a file
def download_file(file_info, local_dir):
    file_url = file_info['download_url']
    file_name = file_info['name']
    file_path = os.path.join(local_dir, file_name)

    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"File {file_name} already exists. Skipping download.")
        return None, None

    # Download the file
    file_response = requests.get(file_url)
    if file_response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(file_response.content)
        return file_path, file_info
    else:
        print(f"Failed to download {file_name}: {file_response.status_code} - {file_response.text}")
        return None, None

# Function to get file metadata
def get_file_metadata(file_info):
    # Get the latest commit for the file
    commits_url = f"https://api.github.com/repos/{GITHUB_REPO}/commits?path={file_info['path']}"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    commit_response = requests.get(commits_url, headers=headers)
    if commit_response.status_code == 200:
        commit_data = commit_response.json()
        if commit_data:
            latest_commit = commit_data[0]  # Get the latest commit
            return {
                'file_location': file_info['path'],
                'creation_date': latest_commit['commit']['committer']['date'],
                'size': file_info['size'],
                'commit_message': latest_commit['commit']['message']
            }
    return None

# Recursive function to process files and directories
def process_directory(url):
    files_metadata = []
    contents = fetch_files(url)

    for item in contents:
        if item['type'] == 'file':
            if item['name'].endswith('.py'):
                local_dir = LOCAL_PYTHON_DIR
            elif item['name'].endswith('.txt'):
                local_dir = LOCAL_TEXT_DIR
            else:
                continue  # Skip other file types

            # Download the file and get metadata
            local_path, item_info = download_file(item, local_dir)
            if local_path and item_info:
                metadata = get_file_metadata(item_info)
                if metadata:
                    files_metadata.append(metadata)
        elif item['type'] == 'dir':
        # Recursively process the subdirectory
            subdirectory_url = item['url']
            files_metadata.extend(process_directory(subdirectory_url))

    return files_metadata

# Function to display a loading spinner
def loading_spinner():
    spinner = ['-', '\\', '|', '/']
    while not processing_done.is_set():
        for symbol in spinner:
            sys.stdout.write(f'\rProcessing... {symbol}')
            sys.stdout.flush()
            time.sleep(0.1)

# Main function to process the repository
def main():
    global processing_done
    processing_done = threading.Event()  # Event to signal when processing is done

    # Start the loading spinner in a separate thread
    spinner_thread = threading.Thread(target=loading_spinner)
    spinner_thread.start()

    files_metadata = process_directory(BASE_URL)

    # Signal that processing is done
    processing_done.set()
    spinner_thread.join()  # Wait for the spinner thread to finish

    # Write metadata to CSV
    try:
        with open(CSV_FILE, mode='w', newline='') as csv_file:
            fieldnames = ['file_location', 'creation_date', 'size', 'commit_message']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for metadata in files_metadata:
                writer.writerow(metadata)

        print(f"\nDownloaded files and created {CSV_FILE} with metadata.")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

if __name__ == "__main__":
    main()
