import os
import requests
import csv
import dotenv
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Load environment variables
dotenv.load_dotenv()

# Configuration
GITHUB_REPO = input("Enter the GitHub repository (e.g., 'username/repo'): ")
BASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/"
LOCAL_DIR = "local_repo"
PYTHON_DIR = os.path.join(LOCAL_DIR, "Python")
TEXT_DIR = os.path.join(LOCAL_DIR, "Text")

# Set maximum files for each type
MAX_PYTHON_FILES = int(os.getenv("MAX_PYTHON_FILES", 5))
MAX_TEXT_FILES = int(os.getenv("MAX_TEXT_FILES", 5))

# Get GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if GITHUB_TOKEN is None:
    raise ValueError("GitHub token is not set. Please set the GITHUB_TOKEN environment variable.")

# Create local directories
os.makedirs(PYTHON_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

metadata = []
total_python_files_downloaded = 0
total_text_files_downloaded = 0
lock = Lock()  # Create a lock for thread-safe updates

def fetch_files(url):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_file_metadata(file_path):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    commits_url = f"https://api.github.com/repos/{GITHUB_REPO}/commits?path={file_path}&per_page=1"
    response = requests.get(commits_url, headers=headers)
    response.raise_for_status()

    commits = response.json()
    if commits:  # Check if the list is not empty
        commit_info = commits[0]  # Get the latest commit info
        creation_date = commit_info['commit']['committer']['date']
        commit_message = commit_info['commit']['message']
        return creation_date, commit_message
    else:
        return 'N/A', 'N/A'

def download_file(file_url, save_dir, file_name):
    global total_python_files_downloaded, total_text_files_downloaded
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    file_response = requests.get(file_url, headers=headers)
    file_response.raise_for_status()

    # Handle duplicate filenames
    new_file_name = file_name
    counter = 1
    while os.path.exists(os.path.join(save_dir, new_file_name)):
        base_name, extension = os.path.splitext(file_name)
        new_file_name = f"{base_name}_{counter}{extension}"
        counter += 1

    with open(os.path.join(save_dir, new_file_name), 'wb') as f:
        f.write(file_response.content)

    # Get creation date and commit message
    creation_date, commit_message = get_file_metadata(new_file_name)

    # Collect metadata
    metadata.append({
        'File Location': os.path.join(save_dir, new_file_name),
        'Creation Date': creation_date,
        'Size (bytes)': len(file_response.content),
        'Commit Message': commit_message
    })

    # Increment the appropriate counter in a thread-safe manner
    with lock:
        if save_dir == PYTHON_DIR:
            total_python_files_downloaded += 1
        elif save_dir == TEXT_DIR:
            total_text_files_downloaded += 1

def process_directory(url):
    global total_python_files_downloaded, total_text_files_downloaded
    items = fetch_files(url)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for item in items:
            # Check if the maximum number of files has been downloaded
            with lock:
                if total_python_files_downloaded >= MAX_PYTHON_FILES and total_text_files_downloaded >= MAX_TEXT_FILES:
                    break  # Stop if the maximum number of files has been downloaded for both types

            if item['type'] == 'file':
                if item['name'].endswith('.py') and total_python_files_downloaded < MAX_PYTHON_FILES:
                        futures.append(executor.submit(download_file, item['download_url'], PYTHON_DIR, item['name']))
                elif item['name'].endswith(('.txt', '.md')) and total_text_files_downloaded < MAX_TEXT_FILES:
                        futures.append(executor.submit(download_file, item['download_url'], TEXT_DIR, item['name']))
            elif item['type'] == 'dir':
                    subdirectory_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{item['path']}"
                    process_directory(subdirectory_url)  # Recursively process subdirectories

                # Wait for all futures to complete
        for future in futures:
            future.result()  # This will raise any exceptions that occurred during the download

# Start processing from the base URL
print("Starting the download process... Please wait.")
start_time = time.time()
process_directory(BASE_URL)

# Calculate total processing time
end_time = time.time()
processing_time = end_time - start_time

# Write metadata to CSV
csv_file_path = os.path.join(LOCAL_DIR, 'file_metadata.csv')
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['File Location', 'Creation Date', 'Size (bytes)', 'Commit Message'])
    writer.writeheader()
    writer.writerows(metadata)

# Print completion message with processing time
print(f"Process completed. {total_python_files_downloaded} Python files and {total_text_files_downloaded} text files downloaded.")
print(f"Metadata saved to {csv_file_path}.")
print(f"Total processing time: {processing_time:.2f} seconds.")
