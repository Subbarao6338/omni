import os
import requests
import csv
import time
import sys
import threading

# Configuration
GITHUB_REPO = "Subbarao6338/subbu-apps-practise-coding"
BASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
LOCAL_DIR = "local_repo"
PYTHON_DIR = os.path.join(LOCAL_DIR, "Python")
TEXT_DIR = os.path.join(LOCAL_DIR, "Text")
MAX_FILES = 5

# Your GitHub personal access token
GITHUB_TOKEN = "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"  # Replace with your token

# Create local directories
os.makedirs(PYTHON_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)


# Function to fetch files from GitHub
def fetch_files(url, file_count):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    contents = response.json()

    for item in contents:
        if item['type'] == 'file':
            if item['name'].endswith('.py') and file_count['py'] < MAX_FILES:
                download_file(item['download_url'], PYTHON_DIR, item['name'], item)
                file_count['py'] += 1
            elif item['name'].endswith(('.txt', '.md')) and file_count['text'] < MAX_FILES:
                download_file(item['download_url'], TEXT_DIR, item['name'], item)
                file_count['text'] += 1
        elif item['type'] == 'dir':
            fetch_files(item['url'], file_count)


# Function to download a file and save metadata
def download_file(file_url, save_dir, file_name, item):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    file_response = requests.get(file_url, headers=headers)
    file_response.raise_for_status()

    # Save the file
    with open(os.path.join(save_dir, file_name), 'wb') as f:
        f.write(file_response.content)

    # Collect metadata
    metadata.append({
        'File Location': os.path.join(save_dir, file_name),
        'Creation Date': 'N/A',  # Set to 'N/A' since we can't get this from the contents endpoint
        'Size (bytes)': item['size'],
        'Commit Message': 'N/A'  # Set to 'N/A' since we can't get this from the contents endpoint
    })


# Function to show a loading spinner
def loading_spinner():
    spinner = ['|', '/', '-', '\\']
    while not loading_done:
        for symbol in spinner:
            sys.stdout.write(f'\rProcessing... {symbol}')
            sys.stdout.flush()
            time.sleep(0.1)


# Start the timer
start_time = time.time()

# Initialize metadata list and file count
metadata = []
file_count = {'py': 0, 'text': 0}
loading_done = False

# Start the loading spinner in a separate thread
spinner_thread = threading.Thread(target=loading_spinner)
spinner_thread.start()

# Fetch files from the GitHub repository
fetch_files(BASE_URL, file_count)

# Stop the loading spinner
loading_done = True
spinner_thread.join()

# Write metadata to CSV
csv_file_path = os.path.join(LOCAL_DIR, 'file_metadata.csv')
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['File Location', 'Creation Date', 'Size (bytes)', 'Commit Message']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in metadata:
        writer.writerow(data)

# End the timer
end_time = time.time()
print(f"\nProcess completed in {end_time - start_time:.2f} seconds.")
print(f"Metadata saved to {csv_file_path}.")
