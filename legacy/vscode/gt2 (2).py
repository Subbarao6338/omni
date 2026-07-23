import os
import requests
import csv
import datetime
import hashlib
import dotenv
from tabulate import tabulate

# Load environment variables from a .env file
dotenv.load_dotenv("./Config/.env")
# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Replace with your GitHub Personal Access Token
REPO_OWNER = "Subbarao6338"  # Replace with the repository owner/organization
REPO_NAME = "subbu-apps-practise-coding"  # Replace with the repository name
LOCAL_REPO_PATH = "local_repo"

def get_latest_commit_sha(branch_name):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{branch_name}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["commit"]["sha"]

def get_file_commits(file_path):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    commits_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits?path={file_path}"
    response = requests.get(commits_url, headers=headers)
    response.raise_for_status()
    return response.json()

def download_file(file_data, local_path):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    file_url = file_data["url"]
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    with open(local_path, "wb") as f:
        f.write(response.content)
    return len(response.content)

def file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    branch_name = "main"
    os.makedirs(LOCAL_REPO_PATH, exist_ok=True)
    os.makedirs(os.path.join(LOCAL_REPO_PATH, "Python"), exist_ok=True)
    os.makedirs(os.path.join(LOCAL_REPO_PATH, "Text"), exist_ok=True)

    metadata = []
    downloaded_files = set()

    latest_commit_sha = get_latest_commit_sha(branch_name)
    tree_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{latest_commit_sha}?recursive=1"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    tree_response = requests.get(tree_url, headers=headers)
    tree_response.raise_for_status()
    github_files = tree_response.json()["tree"]

    for file_data in github_files:
        if file_data["type"] == "blob":
            file_path_in_repo = file_data["path"]

            # Only process Python, Text, and Markdown files
            if not file_path_in_repo.endswith((".py", ".txt", ".md")):
                continue

            # Get the commit history for the specific file
            commits = get_file_commits(file_path_in_repo)
            if commits:
                latest_commit = commits[0]  # Get the most recent commit
                commit_timestamp = datetime.datetime.fromisoformat(latest_commit["commit"]["committer"]["date"].replace("Z", "+00:00")).strftime("%Y%m%d%H%M%S")
                commit_message = latest_commit["commit"]["message"].replace('\n', ' ')
            else:
                commit_timestamp = "N/A"
                commit_message = "N/A"

            # Check if the file has already been downloaded
            if (REPO_NAME, file_path_in_repo, commit_timestamp) in downloaded_files:
                status = "Skipped (Already Downloaded)"
                metadata.append([os.path.join(LOCAL_REPO_PATH, "metadata.csv"),
                                 f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{branch_name}/{file_path_in_repo}", None,
                                 commit_timestamp, commit_message, status])
                continue

            downloaded_files.add((REPO_NAME, file_path_in_repo, commit_timestamp))

            # Determine the local directory based on file type
            local_dir = os.path.join(LOCAL_REPO_PATH,
                                      "Python" if file_path_in_repo.endswith(".py") else "Text")
            local_file_path = os.path.join(local_dir, os.path.basename(file_path_in_repo))

            # Check if the file exists locally and has the same content
            if os.path.exists(local_file_path):
                if file_hash(local_file_path) == file_data["sha"]:
                    status = "Skipped (No Changes)"
                    metadata.append([local_file_path,
                                     f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{branch_name}/{file_path_in_repo}",
                                     os.path.getsize(local_file_path), commit_timestamp, commit_message, status])
                    continue

            # Handle duplicate filenames with the same commit timestamp
            counter = 1
            while os.path.exists(local_file_path):
                base, ext = os.path.splitext(os.path.basename(file_path_in_repo))
                local_file_path = os.path.join(local_dir, f"{base}_{counter}{ext}")
                counter += 1

            # Download the file
            file_size = download_file(file_data, local_file_path)
            status = "Downloaded"
            metadata.append([local_file_path,
                             f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{branch_name}/{file_path_in_repo}",
                             file_size, commit_timestamp, commit_message, status])

    # Write metadata to CSV
    with open(os.path.join(LOCAL_REPO_PATH, "metadata.csv"), "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Local File Path", "GitHub URL", "Size", "Commit Timestamp", "Commit Message", "Status"])
        writer.writerows(metadata)

    # Print the metadata in a tabulated format
    print(tabulate(metadata, headers="keys", tablefmt="simple"))

if __name__ == "__main__":
    main()

