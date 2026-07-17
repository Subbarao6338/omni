import os
import time
import requests
import csv
import datetime
import hashlib
import dotenv
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from a .env file
dotenv.load_dotenv("./Config/.env")

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "Subbarao6338"  # Replace with the repository owner/organization
REPO_NAME = "subbu-apps-practise-coding"  # Replace with the repository name
LOCAL_REPO_PATH = "local_repo"
BRANCH_NAME = "main"  # Default branch
FILE_LIMIT = 100  # Limit the number of files to process
MAX_WORKERS = 5  # Number of parallel downloads

# Create local directories
os.makedirs(LOCAL_REPO_PATH, exist_ok=True)
os.makedirs(os.path.join(LOCAL_REPO_PATH, "Python"), exist_ok=True)
os.makedirs(os.path.join(LOCAL_REPO_PATH, "Text"), exist_ok=True)

# Caching for commit history
commit_cache = {}


def get_latest_commit_sha(branch_name):
    """Fetch the latest commit SHA for the specified branch."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{branch_name}"
    response = fetch_with_retries(url, headers=headers)
    response.raise_for_status()
    return response.json()["commit"]["sha"]


def get_file_commits(file_path):
    """Fetch all commits for a specific file with caching."""
    if file_path in commit_cache:
        return commit_cache[file_path]

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    commits_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits?path={file_path}"
    commits = []
    page = 1

    while True:
        response = fetch_with_retries(f"{commits_url}&page={page}", headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        commits.extend(data)
        page += 1

    commit_cache[file_path] = commits  # Cache the results
    return commits


def download_file(file_data, local_path):
    """Download a file from GitHub and save it to the local path."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    file_url = file_data["url"]
    response = fetch_with_retries(file_url, headers=headers, stream=True)  # Stream the response
    response.raise_for_status()

    # Write the file in chunks to avoid memory issues
    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):  # Write in chunks
            f.write(chunk)

    return os.path.getsize(local_path)  # Return the size of the downloaded file


def file_hash(filepath):
    """Calculate the SHA-1 hash of a file."""
    hasher = hashlib.sha1()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def fetch_with_retries(url, headers, retries=3):
    """Fetch data from a URL with retries on failure."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                raise  # Re-raise the last exception if all attempts fail

def compare_file_contents(file_path, github_file_data):
    """Compare the contents of a local file with the GitHub file using hash."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    file_url = github_file_data["url"]
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    github_file_hash = hashlib.sha1(response.content).hexdigest()  # Get GitHub file hash
    local_file_hash = file_hash(file_path)  # Calculate local file hash

    return local_file_hash == github_file_hash  # Return comparison result


def process_file(file_data, downloaded_files):
    """Process a single file, downloading and comparing as necessary."""
    metadata = []  # List to store metadata for each processed file
    file_path_in_repo = file_data["path"]

    if not file_path_in_repo.endswith((".py", ".txt", ".md")):  # Filter by file types
        return metadata

    # Get the commit information
    commits = get_file_commits(file_path_in_repo)
    if commits:
        latest_commit = commits[0]
        commit_timestamp = datetime.datetime.fromisoformat(
            latest_commit["commit"]["committer"]["date"].replace("Z", "+00:00")).strftime("%Y-%m-%d-%H-%M-%S")
        commit_message = latest_commit["commit"]["message"].replace('\n', ' ')
    else:
        commit_timestamp = "N/A"
        commit_message = "N/A"

    # Remove prefixes and suffixes from the file name
    base_file_name = os.path.basename(file_path_in_repo)
    clean_file_name = base_file_name.split('.')[0]  # Remove suffix
    file_extension = os.path.splitext(base_file_name)[1]

    # Handle duplicate file names
    if clean_file_name in downloaded_files:
        downloaded_files[clean_file_name] += 1
        clean_file_name = f"{clean_file_name}_{downloaded_files[clean_file_name]}{file_extension}"
    else:
        downloaded_files[clean_file_name] = 1

    # Include the directory structure in the local file path
    dir_structure = os.path.dirname(file_path_in_repo).replace('/', '_').replace('\\', '_')
    local_dir = os.path.join(LOCAL_REPO_PATH, "Python" if file_path_in_repo.endswith(".py") else "Text")
    local_file_path = os.path.join(local_dir, f"{BRANCH_NAME}_{dir_structure}_{clean_file_name}_{commit_timestamp}{file_extension}")

    # Check if the local file exists
    if os.path.exists(local_file_path):
        # Compare contents using hash
        if compare_file_contents(local_file_path, file_data):
            print(f"Processing file: {file_path_in_repo} - Skipped (No Changes)")
            metadata.append([local_file_path,
                             f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH_NAME}/{file_path_in_repo}",
                             os.path.getsize(local_file_path), commit_timestamp, commit_message,
                             "Skipped (No Changes)"])
        else:
            print(f"Processing file: {file_path_in_repo} - File has changed, downloading again.")
            # Download the file
            file_size = download_file(file_data, local_file_path)
            print(f"Processing file: {file_path_in_repo} - Downloaded")
            metadata.append([local_file_path,
                             f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH_NAME}/{file_path_in_repo}",
                             file_size, commit_timestamp, commit_message, "Downloaded"])
    else:
        # Download the file if it doesn't exist
        file_size = download_file(file_data, local_file_path)
        print(f"Processing file: {file_path_in_repo} - Downloaded")
        metadata.append([local_file_path,
                         f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH_NAME}/{file_path_in_repo}",
                         file_size, commit_timestamp, commit_message, "Downloaded"])

    return metadata

def write_metadata_to_csv(metadata, csv_path):
    """Write metadata to CSV in chunks."""
    # keys = ["Local File Path", "GitHub URL", "Size", "Commit Timestamp", "Commit Message", "Status"]
    with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(metadata)

def main():
    """Main function to orchestrate the downloading of files and saving metadata."""
    start_time = time.time()  # Start timer
    downloaded_files = {}  # Dictionary to track downloaded files
    latest_commit_sha = get_latest_commit_sha(BRANCH_NAME)
    tree_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{latest_commit_sha}?recursive=1"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    tree_response = requests.get(tree_url, headers=headers)
    tree_response.raise_for_status()
    github_files = tree_response.json()["tree"]

    # Prepare metadata CSV file
    keys = ["Local File Path", "GitHub URL", "Size", "Commit Timestamp", "Commit Message", "Status"]
    metadata_csv_path = os.path.join(LOCAL_REPO_PATH, "metadata.csv")
    with open(metadata_csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)

    # Process the files in parallel
    metadata = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {executor.submit(process_file, file_data, downloaded_files): file_data for file_data in github_files if file_data["type"] == "blob"}

        for future in as_completed(future_to_file):
            result = future.result()
            if result:
                metadata.extend(result)

    # Write all metadata to CSV at once
    if metadata:
        write_metadata_to_csv(metadata, metadata_csv_path)

    print(f"Process completed. Metadata saved to {metadata_csv_path}.")
    print(f"Total processing time: {time.time() - start_time:.2f} seconds.")

    # Display the metadata in a table format
    print(tabulate(metadata, headers=keys, tablefmt="simple"))


if __name__ == "__main__":
    main()

