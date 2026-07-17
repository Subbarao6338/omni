import os
import git
import pandas as pd
from datetime import datetime
import shutil
import logging

# Configuration
REPO_URL = 'https://github.com/ayush8853/ayush_pandey.git'  # GitHub repository URL
LOCAL_DIR = 'local_repo'  # Local directory to clone the repo
PYTHON_DIR = 'Python'  # Directory for .py files
TEXT_DIR = 'Text'  # Directory for .txt files
CSV_FILE = 'file_metadata.csv'  # Output CSV file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clone the repository if it doesn't exist
if not os.path.exists(LOCAL_DIR):
    try:
        git.Repo.clone_from(REPO_URL, LOCAL_DIR)
        logging.info(f"Cloned repository from {REPO_URL} to {LOCAL_DIR}.")
    except Exception as e:
        logging.error(f"Failed to clone repository: {e}")
        exit(1)

# Create directories for .py and .txt files
os.makedirs(PYTHON_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

# Prepare metadata storage
metadata = []

# Walk through the cloned repository
repo = git.Repo(LOCAL_DIR)
for root, _, files in os.walk(LOCAL_DIR):
    for file in files:
        file_path = os.path.join(root, file)
        if file.endswith('.py'):
            # Copy .py files
            dest_path = os.path.join(PYTHON_DIR, file)
            try:
                shutil.copy(file_path, dest_path)
                logging.info(f"Copied {file_path} to {dest_path}.")
                # Collect metadata
                commit_message = repo.head.commit.message.strip()
                metadata.append({
                    'File Location': dest_path,
                    'Creation Date': datetime.fromtimestamp(os.path.getctime(dest_path)),
                    'Size (bytes)': os.path.getsize(dest_path),
                    'Commit Message': commit_message
                })
            except Exception as e:
                logging.error(f"Failed to copy {file_path}: {e}")
        elif file.endswith('.txt'):
            # Copy .txt files
            dest_path = os.path.join(TEXT_DIR, file)
            try:
                shutil.copy(file_path, dest_path)
                logging.info(f"Copied {file_path} to {dest_path}.")
                # Collect metadata
                commit_message = repo.head.commit.message.strip()
                metadata.append({
                    'File Location': dest_path,
                    'Creation Date': datetime.fromtimestamp(os.path.getctime(dest_path)),
                    'Size (bytes)': os.path.getsize(dest_path),
                    'Commit Message': commit_message
                })
            except Exception as e:
                logging.error(f"Failed to copy {file_path}: {e}")

# Create a DataFrame and save to CSV
df = pd.DataFrame(metadata)
df.to_csv(CSV_FILE, index=False)
logging.info(f"Files copied and metadata saved to {CSV_FILE}.")
