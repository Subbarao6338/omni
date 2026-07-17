import os
import subprocess
import sys
import time
import threading


def check_ruff_installed():
    """Check if ruff is installed."""
    try:
        # Attempt to run ruff to check if it's installed
        subprocess.run(['ruff', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: Ruff is not installed or not found in your PATH. Please install it using 'pip install ruff'.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error checking ruff version: {e.stderr.decode()}")
        sys.exit(1)


def review_files(folder, loading_event):
    report = []
    if not os.path.exists(folder):
        print(f"Error: The folder '{folder}' does not exist.")
        return report

    for root, _, files in os.walk(folder):  # Use os.walk to include subdirectories
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith('.py'):
                # Review Python files with ruff
                result = subprocess.run(['ruff', file_path], capture_output=True, text=True)
                report.append({
                    'file': file_path,
                    'type': 'Python',
                    'output': result.stdout.strip(),
                    'error': result.stderr.strip(),
                    'return_code': result.returncode
                })
    loading_event.set()  # Signal that processing is complete
    return report


def generate_report(report):
    with open('review_report_ruff.txt', 'w') as f:
        for entry in report:
            f.write(f"File: {entry['file']}\n")
            f.write(f"Type: {entry['type']}\n")
            f.write("Output:\n")
            f.write(entry['output'] if entry['output'] else "No issues found.\n")
            f.write("Errors:\n")
            f.write(entry['error'] if entry['error'] else "No errors.\n")
            f.write("\n" + "=" * 40 + "\n")


def loading_screen(loading_event):
    """Display a loading screen while processing."""
    loading_symbols = ['|', '/', '-', '\\']
    idx = 0
    while not loading_event.is_set():
        print(f"\rProcessing files... {loading_symbols[idx]}", end="")
        idx = (idx + 1) % len(loading_symbols)
        time.sleep(0.1)
    print("\rProcessing files... Done!      ")


def review():
    check_ruff_installed()  # Check if ruff is installed
    folder_to_review = input("Enter the path of the folder to review: ")  # Get folder path from user
    combined_report = []

    loading_event = threading.Event()
    loading_thread = threading.Thread(target=loading_screen, args=(loading_event,))
    loading_thread.start()

    # Review the files in the specified folder
    review_report = review_files(folder_to_review, loading_event)
    combined_report.extend(review_report)  # Combine reports from the specified folder

    loading_event.set()  # Ensure the loading thread exits
    loading_thread.join()  # Wait for the loading thread to finish

    if combined_report:
        # Generate a summary report
        generate_report(combined_report)
        print("File review completed. Check 'review_report_ruff.txt' for details.")
    else:
        print("No Python files found for review.")

if __name__ == "__main__":
    review()
