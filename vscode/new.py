import os
import requests
import csv

# Function to fetch GitHub repository content
def fetch_github_content(repo_url):
    parts = repo_url.split('/')
    owner = parts[3]
    repo = parts[4]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Failed to fetch repository content: {response.status_code}")
        return []

    return response.json()

# Function to download a file
def download_file(file_url, save_path):
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download {file_url}: {response.status_code}")

# Function to get last modified date of a file
def get_last_modified(owner, repo, file_path):
    commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits?path={file_path}&per_page=1"
    response = requests.get(commit_url)
    if response.status_code == 200:
        commits = response.json()
        if commits:
            return commits[0]['commit']['committer']['date']
    return 'Unknown'

# Function to process files and save metadata
def process_files(repo_content, base_path, owner, repo):
    python_folder = os.path.join(base_path, "python")
    text_folder = os.path.join(base_path, "text")
    os.makedirs(python_folder, exist_ok=True)
    os.makedirs(text_folder, exist_ok=True)

    metadata = []

    for item in repo_content:
        if item['type'] == 'file':
            file_name = item['name']
            file_url = item['download_url']
            file_path = os.path.join(
                python_folder if file_name.endswith('.py') else text_folder if file_name.endswith(('.txt', '.md')) else base_path,
                file_name
            )

            if file_url and (file_name.endswith('.py') or file_name.endswith(('.txt', '.md'))):
                download_file(file_url, file_path)
                last_modified = get_last_modified(owner, repo, item['path'])
                metadata.append({
                    'File Name': file_name,
                    'File URL': file_url,
                    'Local Path': file_path,
                    'Size (bytes)': item.get('size', 'Unknown'),
                    'Last Modified': last_modified
                })
        elif item['type'] == 'dir':
            # Fetch contents of the directory
            dir_path = item['path']
            dir_content = fetch_github_directory_contents(owner, repo, dir_path)
            metadata.extend(process_files(dir_content, base_path, owner, repo))

    return metadata

# Function to fetch contents of a directory
def fetch_github_directory_contents(owner, repo, path):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    print(f"Fetching directory contents from: {api_url}")
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Error fetching directory contents: {response.text}")
        return []

    return response.json()

# Function to save metadata to a CSV file
def save_metadata_to_csv(metadata, csv_path):
    if not metadata:
        print("No metadata to save.")
        return

    keys = metadata[0].keys()
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(metadata)
    print(f"Metadata saved to: {csv_path}")

# Main function
def main():
    repo_url = "https://github.com/Subbarao6338/subbu-apps-practise-coding"
    base_path = "downloaded_files"
    os.makedirs(base_path, exist_ok=True)
    csv_file_path = os.path.join(base_path, "file_metadata.csv")

    print(f"Fetching repository content from: {repo_url}")
    repo_content = fetch_github_content(repo_url)

    if repo_content:
        parts = repo_url.split('/')
        owner = parts[3]
        repo = parts[4]

        # Process files and collect metadata
        metadata = process_files(repo_content, base_path, owner, repo)

        # Save metadata to CSV
        save_metadata_to_csv(metadata, csv_file_path)
        print(f"Downloaded files and metadata saved to: {base_path}")
    else:
        print("No files to process or an error occurred.")

if __name__ == "__main__":
    main()
