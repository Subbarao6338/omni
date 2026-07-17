import os
import subprocess
import sys
import time
import threading


def check_mypy_installed():
    """Check if mypy is installed."""
    try:
        # Attempt to run mypy to check if it's installed
        subprocess.run(['mypy', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: mypy is not installed or not found in your PATH. Please install it using 'pip install mypy'.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error checking mypy version: {e.stderr.decode()}")
        sys.exit(1)


def review_files(folder, loading_event):
    report = []
    if not os.path.exists(folder):
        print(f"Error: The folder '{folder}' does not exist.")
        return report

    python_files_found = False

    for root, _, files in os.walk(folder):  # Use os.walk to include subdirectories
        for filename in files:
            if filename.endswith('.py'):
                python_files_found = True
                file_path = os.path.join(root, filename)
                # Review Python files with mypy
                result = subprocess.run(['mypy', file_path], capture_output=True, text=True)
                report.append({
                    'file': file_path,
                    'type': 'Python',
                    'output': result.stdout.strip(),
                    'error': result.stderr.strip(),
                    'return_code': result.returncode
                })

    loading_event.set()  # Signal that processing is complete
    if not python_files_found:
        print("No Python files found in the specified folder.")
    return report


def generate_report(report):
    with open('review_report_mypy.txt', 'w') as f:
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
    check_mypy_installed()  # Check if mypy is installed
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
        print("File review completed. Check 'review_report_mypy.txt' for details.")
    else:
        print("No Python files found for review.")

if __name__ == "__main__":
    review()
