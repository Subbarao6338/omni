import os
import requests
import csv
import time
import dotenv  # To load environment variables from a .env file
import threading
import sys

# Load environment variables from .env file
dotenv.load_dotenv()

# Configuration
GITHUB_REPO = input("Enter the GitHub repository (e.g., 'username/repo'): ")  # Get repo from user input
BASE_URL = f"{os.getenv('GITHUB_REPO')}{GITHUB_REPO}/contents/"
LOCAL_PYTHON_DIR = "Python"
LOCAL_TEXT_DIR = "Text"
CSV_FILE = "file_metadata.csv"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Get token from environment variable

if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")

# Create local directories if they don't exist
os.makedirs(LOCAL_PYTHON_DIR, exist_ok=True)
os.makedirs(LOCAL_TEXT_DIR, exist_ok=True)

# Function to check rate limit
def check_rate_limit():
    response = requests.get(os.getenv("GITHUB_RATE_LIMIT"), headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if response.status_code == 200:
        rate_limit_info = response.json()
        remaining = rate_limit_info['rate']['remaining']
        reset_time = rate_limit_info['rate']['reset']
        return remaining, reset_time
    return None, None

# Function to fetch files from GitHub repository
def fetch_files(url):
    remaining, reset_time = check_rate_limit()
    if remaining is not None and remaining == 0:
        wait_time = reset_time - int(time.time()) + 5  # Wait until the rate limit resets
        print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
        time.sleep(wait_time)

    try:
        response = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch files: {e}")
        return []

# Function to download a file
def download_file(file_info, local_dir):
    file_url = file_info['download_url']
    file_name = file_info['name']
    file_path = os.path.join(local_dir, file_name)

    # Handle filename conflicts
    base, extension = os.path.splitext(file_name)
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(local_dir, f"{base}_{counter}{extension}")
        counter += 1

    # Download the file
    try:
        file_response = requests.get(file_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        file_response.raise_for_status()  # Raise an error for bad responses
        with open(file_path, 'wb') as f:
            f.write(file_response.content)
        return file_path, file_info
    except requests.RequestException as e:
        print(f"Failed to download {file_name}: {e}")
        return None, None

# Function to get file metadata
def get_file_metadata(file_info):
    # Get the latest commit for the file
    commits_url = f"{os.getenv('GITHUB_REPO')}{GITHUB_REPO}/commits?path={file_info['path']}"
    commit_response = requests.get(commits_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
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
    else:
        print(f"Failed to fetch commit data for {file_info['path']}: {commit_response.status_code}")
    return None

# Function to display loading animation
def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\rProcessing files: {animation[idx]}')
        sys.stdout.flush()
        idx = (idx + 1) % len(animation)
        time.sleep(0.1)  # Adjust the speed of the animation
    print("\rProcessing files... Done!      ")

# Recursive function to process directories and files
def process_directory(url, local_dir, files_metadata, file_counts):
    contents = fetch_files(url)

    for item in contents:
        if item['type'] == 'file':
            if item['name'].endswith('.py'):
                if file_counts['python'] >= 10:  # Limit to 10 Python files
                    continue
                local_subdir = LOCAL_PYTHON_DIR
                file_counts['python'] += 1  # Increment counter for Python files

            elif item['name'].endswith('.txt') or item['name'].endswith('.md'):
                if file_counts['text'] >= 10:  # Limit to 10 text files
                    continue
                local_subdir = LOCAL_TEXT_DIR
                file_counts['text'] += 1  # Increment counter for text files

            else:
                continue  # Skip other file types

            # Download the file and get metadata
            local_path, item_info = download_file(item, local_subdir)
            if local_path and item_info:
                metadata = get_file_metadata(item_info)
                if metadata:
                    files_metadata.append(metadata)

        elif item['type'] == 'dir':
            # Recursively process the subdirectory, passing the updated counts
            subdirectory_url = item['url']
            process_directory(subdirectory_url, local_dir, files_metadata, file_counts)

def main():
    files_metadata = []
    stop_event = threading.Event()  # Event to stop the loading animation

    # Start the loading animation in a separate thread
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    loading_thread.start()

    # Initialize file counts
    file_counts = {'python': 0, 'text': 0}

    # Process the root directory
    process_directory(BASE_URL, LOCAL_PYTHON_DIR, files_metadata, file_counts)

    # Stop the loading animation
    stop_event.set()
    loading_thread.join()  # Wait for the loading thread to finish

    # Write metadata to CSV only if there is metadata to write
    if files_metadata:
        with open(CSV_FILE, mode='w', newline='') as csv_file:
            fieldnames = ['file_location', 'creation_date', 'size', 'commit_message']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for metadata in files_metadata:
                writer.writerow(metadata)

        print(f"\nDownloaded files and created {CSV_FILE} with metadata.")
    else:
        print("\nNo files were downloaded or metadata was collected.")

if __name__ == "__main__":
    main()
