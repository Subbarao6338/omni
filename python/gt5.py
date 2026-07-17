import os
import time
import requests
import csv
import datetime
# import hashlib
import dotenv
from tabulate import tabulate

# Load environment variables from a .env file
dotenv.load_dotenv("./Config/.env")

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "Subbarao6338"  # Replace with the repository owner/organization
REPO_NAME = "subbu-apps-practise-coding"  # Replace with the repository name
LOCAL_REPO_PATH = "local_repo"
BRANCH_NAME = "main"  # Default branch
FILE_LIMIT = 100  # Limit the number of files to process

# Create local directories
os.makedirs(LOCAL_REPO_PATH, exist_ok=True)
os.makedirs(os.path.join(LOCAL_REPO_PATH, "Python"), exist_ok=True)
os.makedirs(os.path.join(LOCAL_REPO_PATH, "Text"), exist_ok=True)


def get_latest_commit_sha(branch_name):
    """Fetch the latest commit SHA for the specified branch."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{branch_name}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["commit"]["sha"]


def get_file_commits(file_path):
    """Fetch all commits for a specific file."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    commits_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits?path={file_path}"
    commits = []
    page = 1

    while True:
        response = requests.get(f"{commits_url}&page={page}", headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        commits.extend(data)
        page += 1

    return commits   # Return all commits for the file


def download_file(file_data, local_path):
    """Download a file from GitHub and save it to the local path."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    file_url = file_data["url"]
    response = requests.get(file_url, headers=headers, stream=True)  # Stream the response
    response.raise_for_status()

    # Write the file in chunks to avoid memory issues
    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):  # Write in chunks
            f.write(chunk)

    return os.path.getsize(local_path)  # Return the size of the downloaded file


# def file_hash(filepath):
#     hasher = hashlib.sha256()
#     with open(filepath, "rb") as f:
#         while chunk := f.read(4096):
#             hasher.update(chunk)
#     return hasher.hexdigest()


def compare_file_contents(file_path, github_file_data):
    """Compare the contents of a local file with the GitHub file."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    file_url = github_file_data["url"]
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    github_file_content = response.content # Get GitHub file content

    with open(file_path, "rb") as local_file:
        local_file_content = local_file.read() # Read local file content

    return local_file_content == github_file_content # Return comparison result


def process_files(github_files, downloaded_files):
    """Process the list of GitHub files, downloading and comparing as necessary."""
    metadata = []  # List to store metadata for each processed file
    file_counter = {}  # Dictionary to handle duplicate file names
    processed_count = 0  # Counter for processed files

    for file_data in github_files:
        if file_data["type"] == "blob": # Only process blob types (actual files)
            file_path_in_repo = file_data["path"]
            if not file_path_in_repo.endswith((".py", ".txt", ".md")): # Filter by file types
                continue

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
            if clean_file_name in file_counter:
                file_counter[clean_file_name] += 1
                clean_file_name = f"{clean_file_name}_{file_counter[clean_file_name]}{file_extension}"
            else:
                file_counter[clean_file_name] = 1

            # Include the directory structure in the local file path
            dir_structure = os.path.dirname(file_path_in_repo).replace('/', '_').replace('\\', '_')
            local_dir = os.path.join(LOCAL_REPO_PATH, "Python" if file_path_in_repo.endswith(".py") else "Text")
            local_file_path = os.path.join(local_dir, f"{BRANCH_NAME}_{dir_structure}_{clean_file_name}_{commit_timestamp}{file_extension}")
            unique_file_id = (REPO_NAME, clean_file_name, commit_timestamp)

            print(f"Processing file: {file_path_in_repo}", end=" - ")

            if unique_file_id in downloaded_files:
                print("Skipped (Already Downloaded)")
                metadata.append([os.path.join(LOCAL_REPO_PATH, "metadata.csv"),
                                 f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH_NAME}/{file_path_in_repo}", None,
                                 commit_timestamp, commit_message, "Skipped (Already Downloaded)"])
                continue

            downloaded_files.add(unique_file_id)

            # Check if the local file exists
            if os.path.exists(local_file_path):
                # Compare contents instead of SHA
                if compare_file_contents(local_file_path, file_data):
                    print("Skipped (No Changes)")
                    metadata.append([local_file_path,
                                     f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH_NAME}/{file_path_in_repo}",
                                     os.path.getsize(local_file_path), commit_timestamp, commit_message,
                                     "Skipped (No Changes)"])
                    continue
                else:
                    print("File has changed, downloading again.")

            # Download the file if it doesn't exist or has changed
            file_size = download_file(file_data, local_file_path)
            print("Downloaded")
            metadata.append([local_file_path,
                             f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH_NAME}/{file_path_in_repo}",
                             file_size, commit_timestamp, commit_message, "Downloaded"])

            processed_count += 1
            if processed_count >= FILE_LIMIT:
                print(f"Reached file limit of {FILE_LIMIT}. Stopping further processing.")
                break

    return metadata

def main():
    """Main function to orchestrate the downloading of files and saving metadata."""
    start_time = time.time() # Start timer
    downloaded_files = set() # Set to track downloaded files
    latest_commit_sha = get_latest_commit_sha(BRANCH_NAME)
    tree_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{latest_commit_sha}?recursive=1"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    tree_response = requests.get(tree_url, headers=headers)
    tree_response.raise_for_status()
    github_files = tree_response.json()["tree"]

    # Process the files and gather metadata
    metadata = process_files(github_files, downloaded_files)

    # Write metadata to CSV
    metadata_csv_path = os.path.join(LOCAL_REPO_PATH, "metadata.csv")
    keys = ["Local File Path", "GitHub URL", "Size", "Commit Timestamp", "Commit Message", "Status"]
    with open(metadata_csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerows(metadata)

    print(f"Process completed. Metadata saved to {metadata_csv_path}.")
    print(f"Total processing time: {time.time() - start_time:.2f} seconds.")

    print(tabulate(metadata, headers=keys, tablefmt="simple"))

if __name__ == "__main__":
    main()

