import os
import subprocess
import sys

def check_pylint_installed():
    """Check if pylint is installed."""
    try:
        # Attempt to run pylint to check if it's installed
        subprocess.run(['pylint', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: Pylint is not installed or not found in your PATH. Please install it using 'pip install pylint'.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error checking pylint version: {e.stderr}")
        sys.exit(1)

def review_files(folder):
    report = []
    if not os.path.exists(folder):
        print(f"Error: The folder '{folder}' does not exist.")
        return report

    for root, _, files in os.walk(folder):  # Use os.walk to include subdirectories
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith('.py'):
                # Review Python files with pylint
                result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
                report.append({
                    'file': file_path,
                    'type': 'Python',
                    'output': result.stdout,
                    'error': result.stderr
                })
    return report

def generate_report(report):
    with open('file_review_report.txt', 'w') as f:
        for entry in report:
            f.write(f"File: {entry['file']}\n")
            f.write(f"Type: {entry['type']}\n")
            f.write("Output:\n")
            f.write(entry['output'])
            f.write("Errors:\n")
            f.write(entry['error'])
            f.write("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    check_pylint_installed()  # Check if pylint is installed
    folders_to_review = ["Python"]  # List of folders to review
    combined_report = []

    for folder in folders_to_review:
        review_report = review_files(folder)
        combined_report.extend(review_report)  # Combine reports from both folders

    if combined_report:
        # Generate a summary report
        generate_report(combined_report)
        print("File review completed. Check 'file_review_report.txt' for details.")
    else:
        print("No Python or text files found for review.")
