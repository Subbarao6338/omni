import os
import sys
import logging
from argparse import ArgumentParser
from pylint.lint import Run

# Set up logging to record messages with a specific format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_pylint_installed():
    """Check if pylint is installed."""
    try:
        import pylint  # Attempt to import pylint
    except ImportError:
        # Log an error and exit if pylint is not installed
        logging.error("Pylint is not installed. Please install it using 'pip install pylint'.")
        sys.exit(1)

def review_files(folder, pylint_options=None):
    """Review Python files in the specified folder using pylint."""
    report = []  # Initialize an empty report list
    if not os.path.exists(folder):
        # Log an error if the specified folder does not exist
        logging.error(f"The folder '{folder}' does not exist.")
        return report

    # Collect all Python files in the specified folder and its subdirectories
    python_files = [os.path.join(root, f) for root, _, files in os.walk(folder) for f in files if f.endswith('.py')]
    if not python_files:
        print("No Python files found in the specified folder.")
        return report

    # Iterate over each Python file and run pylint
    for file_path in python_files:
        try:
            # Run pylint on the file and capture the results
            results = Run([file_path] + (pylint_options or []))
            report.append({
                'file': file_path,
                'output': results.linter.reporter,  # Capture the output from pylint
                'error': '',  # No error if pylint runs successfully
                'return_code': results.linter.msg_status  # Capture the return code from pylint
            })
        except Exception as e:
            # If pylint fails, capture the error message
            report.append({
                'file': file_path,
                'output': '',  # No output if there was an error
                'error': str(e),  # Capture the exception message
                'return_code': 2  # Set return code to 2 for errors
            })

    return report  # Return the report containing results for all files

def generate_report(report):
    """Generate a markdown report from the pylint review results."""
    with open('review_report_pylint.md', 'w') as f:
        # Write the report header and return codes section
        f.write("# Pylint Review Report\n\n## Pylint Return Codes:\n")
        f.write("0: No issues found.\n1: One or more issues found.\n2: Pylint encountered an error.\n\n")

        # Write the results for each reviewed file
        for entry in report:
            f.write(f"### File: {entry['file']}\n")
            f.write("### Output:\n```\n" + (entry['output'] or "No issues found.\n") + "\n```\n")
            f.write("### Errors:\n```\n" + (entry['error'] or "No errors.\n") + "\n```\n")
            f.write("### Return Code:\n```\n" + str(entry['return_code']) + "\n```\n\n---\n\n")

def review(pylint_options):
    """Main review function to check Python files using pylint."""
    check_pylint_installed()  # Ensure pylint is installed
    folder_to_review = input("Enter the path of the folder to review: ")  # Get folder path from user

    # Collect all Python files for progress tracking
    python_files = [f for _, _, files in os.walk(folder_to_review) for f in files if f.endswith('.py')]
    total_files = len(python_files)

    if total_files == 0:
        print("No Python files found for review.")
        return  # Exit if no Python files are found

    print(f"Found {total_files} Python files to review. Processing... Please wait.")
    # Review the files and get the report
    report = review_files(folder_to_review, pylint_options)
    # Generate a report if there are results
    if report:
        generate_report(report)
        print("Files review completed. Check 'review_report_pylint.md' for details.")

if __name__ == "__main__":
    # Set up argument parsing for additional pylint options
    parser = ArgumentParser(description="Review Python files using pylint.")
    parser.add_argument('--pylint-options', nargs='*', help='Additional options to pass to pylint.')
    args = parser.parse_args()  # Parse the command-line arguments
    review(args.pylint_options)  # Call the review function
