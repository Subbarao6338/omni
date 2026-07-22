import os
import requests
import csv
import time
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Configuration
# GITHUB_REPO = input("Enter the GitHub repository (e.g., 'username/repo'): ")
GITHUB_REPO = "Subbarao6338/subbu-apps-practise-coding"
BASE_URL = f"{os.getenv('GITHUB_REPO')}{GITHUB_REPO}/contents/"
LOCAL_DIR = "local_repo"
PYTHON_DIR = os.path.join(LOCAL_DIR, "Python")
TEXT_DIR = os.path.join(LOCAL_DIR, "Text")
MAX_FILES = 5
MAX_WORKERS = 5

# Get GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if GITHUB_TOKEN is None:
    raise ValueError("GitHub token is not set. Please set the GITHUB_TOKEN environment variable.")

# Create local directories
os.makedirs(PYTHON_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

metadata = []
file_count = {'py': 0, 'text': 0}
loading_done = False
download_tasks = []

def fetch_files(url):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        for item in response.json():
            if item['type'] == 'file':
                if item['name'].endswith('.py') and file_count['py'] < MAX_FILES:
                    download_tasks.append((item['download_url'], PYTHON_DIR, item['name'], item))
                    file_count['py'] += 1
                elif item['name'].endswith(('.txt', '.md')) and file_count['text'] < MAX_FILES:
                    download_tasks.append((item['download_url'], TEXT_DIR, item['name'], item))
                    file_count['text'] += 1
            elif item['type'] == 'dir':
                fetch_files(item['url'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching files: {e}")

def get_file_metadata(file_path):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    try:
        # Get the commit history for the file
        commits_url = f"{os.getenv('GITHUB_REPO')}{GITHUB_REPO}/commits?path={file_path}&per_page=1"
        response = requests.get(commits_url, headers=headers)
        response.raise_for_status()
        commit_info = response.json()[0]  # Get the latest commit info
        creation_date = commit_info['commit']['committer']['date']
        commit_message = commit_info['commit']['message']
        return creation_date, commit_message
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata for {file_path}: {e}")
        return 'N/A', 'N/A'

def download_file(args):
    file_url, save_dir, file_name, item = args
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    try:
        file_response = requests.get(file_url, headers=headers)
        file_response.raise_for_status()

        # Handle duplicate filenames
        base_name, extension = os.path.splitext(file_name)
        new_file_name = file_name
        counter = 1
        while os.path.exists(os.path.join(save_dir, new_file_name)):
            new_file_name = f"{base_name}_{counter}{extension}"
            counter += 1

        with open(os.path.join(save_dir, new_file_name), 'wb') as f:
            f.write(file_response.content)

        # Get creation date and commit message
        creation_date, commit_message = get_file_metadata(new_file_name)

        metadata.append({
            'File Location': os.path.join(save_dir, new_file_name),
            'Creation Date': creation_date,
            'Size (bytes)': item['size'],
            'Commit Message': commit_message
        })
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file {file_name}: {e}")

def loading_spinner():
    spinner = ['|', '/', '-', '\\']
    while not loading_done:
        for symbol in spinner:
            sys.stdout.write(f'\rLoading... {symbol}')
            sys.stdout.flush()
            time.sleep(0.1)

# Start the loading spinner in a separate thread
spinner_thread = threading.Thread(target=loading_spinner)
spinner_thread.start()

# Fetch files and download them
fetch_files(BASE_URL)
if download_tasks:
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_file, download_tasks)

# Stop the loading spinner
loading_done = True
spinner_thread.join()

# Write metadata to CSV
csv_file_path = os.path.join(LOCAL_DIR, 'file_metadata.csv')
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['File Location', 'Creation Date', 'Size (bytes)', 'Commit Message'])
    writer.writeheader()
    writer.writerows(metadata)

# Print completion message
print(f"\nProcess completed. Metadata saved to {csv_file_path}.")
