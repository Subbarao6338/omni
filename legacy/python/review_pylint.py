import os
import subprocess
import sys
import time
import threading
import logging
from argparse import ArgumentParser

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_pylint_installed():
    """Check if pylint is installed."""
    try:
        subprocess.run(['pylint', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        logging.error(
            "Pylint is not installed or not found in your PATH. Please install it using 'pip install pylint'.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking pylint version: {e.stderr.decode()}")
        sys.exit(1)


def review_files(folder, loading_event, pylint_options=None):
    report = []
    if not os.path.exists(folder):
        logging.error(f"The folder '{folder}' does not exist.")
        return report

    python_files_found = False

    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.endswith('.py'):
                python_files_found = True
                file_path = os.path.join(root, filename)
                command = ['pylint'] + (pylint_options or []) + [file_path]
                try:
                    result = subprocess.run(command, capture_output=True, text=True, check=True)
                    report.append({
                        'file': file_path,
                        'type': 'Python',
                        'output': result.stdout.strip(),
                        'error': '',
                        'return_code': result.returncode
                    })
                except subprocess.CalledProcessError as e:
                    # Log the error to the report but not to the console
                    report.append({
                        'file': file_path,
                        'type': 'Python',
                        'output': e.stdout.strip(),
                        'error': e.stderr.strip(),
                        'return_code': e.returncode
                    })

    loading_event.set()
    if not python_files_found:
        logging.info("No Python files found in the specified folder.")
    return report


def generate_report(report):
    with open('review_report_pylint.md', 'w') as f:
        f.write("# Pylint Review Report\n\n")
        for entry in report:
            f.write(f"### File: {entry['file']}\n")
            f.write(f"**Type:** {entry['type']}\n")
            f.write("### Output:\n")
            f.write("```\n")
            f.write(entry['output'] if entry['output'] else "No issues found.\n")
            f.write("\n")
            f.write("```\n")
            f.write("### Errors:\n")
            f.write("```\n")
            f.write(entry['error'] if entry['error'] else "No errors.\n")
            f.write("```\n")
            f.write("\n---\n\n")  # Use a horizontal rule for separation


def loading_screen(loading_event, total_files):
    """Display a loading screen while processing."""
    loading_symbols = ['|', '/', '-', '\\']
    idx = 0
    processed_files = 0
    while not loading_event.is_set():
        print(f"\rProcessing files... {loading_symbols[idx]} ({processed_files}/{total_files})", end="")
        idx = (idx + 1) % len(loading_symbols)
        time.sleep(0.1)
        if processed_files < total_files:
            processed_files += 1
    print("\rProcessing files... Done!      ")


def review(pylint_options):
    check_pylint_installed()
    folder_to_review = input("Enter the path of the folder to review: ")
    combined_report = []

    # Count only Python files for progress tracking
    total_files = sum(
        [len(files) for _, _, files in os.walk(folder_to_review) if files and any(f.endswith('.py') for f in files)])

    loading_event = threading.Event()
    loading_thread = threading.Thread(target=loading_screen, args=(loading_event, total_files))
    loading_thread.start()

    review_report = review_files(folder_to_review, loading_event, pylint_options)
    combined_report.extend(review_report)

    loading_event.set()
    loading_thread.join()

    if combined_report:
        generate_report(combined_report)
        logging.info("File review completed. Check 'review_report_pylint.md' for details.")
    else:
        logging.info("No Python files found for review.")

if __name__ == "__main__":
    parser = ArgumentParser(description="Review Python files using pylint.")
    parser.add_argument('--pylint-options', nargs='*', help='Additional options to pass to pylint.')
    args = parser.parse_args()

    review(args.pylint_options)
