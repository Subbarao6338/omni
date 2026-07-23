import os
import subprocess
import sys
import logging
import time
# Set up logging to display messages with a specific format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_pylint_installed():
    """Check if pylint is installed."""
    try:
        # Attempt to run pylint to check if it's installed
        subprocess.run(['pylint', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        # If pylint is not found, log an error and exit
        logging.error("Pylint is not installed. Please install it using 'pip install pylint'.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        # Log any errors encountered while checking pylint version
        logging.error(f"Error checking pylint version: {e.stderr.decode()}")
        sys.exit(1)

def review_files(folder, pylint_options=None):
    """Review Python files in the specified folder using pylint."""
    report = []  # Initialize an empty report list
    if not os.path.exists(folder):
        logging.error(f"The folder '{folder}' does not exist.")
        return report

    # Collect all Python files in the specified folder and its subdirectories
    python_files = [os.path.join(root, f) for root, _, files in os.walk(folder) for f in files if f.endswith('.py')]

    if not python_files:
        print("No Python files found in the specified folder.")
        return report

    # Iterate over each Python file and run pylint
    for file_path in python_files:
        command = ['pylint'] + (pylint_options or []) + [file_path]  # Construct the pylint command
        try:
            # Run pylint and capture the output
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            report.append({
                'file': file_path,
                'type': 'Python',
                'output': result.stdout.strip(),  # Capture standard output
                'error': result.stderr.strip(),    # Capture standard error
                'return_code': result.returncode    # Capture return code
            })
        except subprocess.CalledProcessError as e:
            # If pylint fails, capture the output and error
            report.append({
                'file': file_path,
                'type': 'Python',
                'output': e.stdout.strip(),
                'error': e.stderr.strip(),
                'return_code': e.returncode
            })

    return report

def generate_report(report):
    """Generate a markdown report from the pylint review results."""
    with open('review_report_pylint.md', 'w') as f:
        f.write("# Pylint Review Report\n\n")
        # Pylint Return Codes Section
        f.write("## Pylint Return Codes:\n")
        f.write("0: No issues found. The code is clean according to the linting rules.\n")
        f.write("1: One or more issues were found. This indicates that there are linting errors or warnings in the code.\n")
        f.write("2: Pylint was unable to check the code due to an error (e.g., a syntax error in the code being analyzed).\n")
        f.write("4: Pylint was unable to find the specified module or file.\n")
        f.write("8: Pylint encountered a fatal error (e.g., an internal error).\n\n")

        # Write the results for each reviewed file
        for entry in report:
            f.write(f"### File: {entry['file']}\n")
            f.write(f"**Type:** {entry['type']}\n")
            f.write("### Output:\n```\n")
            f.write(entry['output'] or "No issues found.\n")  # Output from pylint
            f.write("\n```\n### Errors:\n```\n")
            f.write(entry['error'] or "No errors.\n")  # Errors from pylint
            f.write("\n```\n### Return Code:\n```\n")
            f.write(str(entry['return_code']) or "N/A.\n")  # Return code from pylint
            f.write("\n```\n\n---\n\n")  # Separator for each file's report

def review(pylint_options):
    """Main review function to check Python files using pylint."""
    check_pylint_installed()  # Ensure pylint is installed
    folder_to_review = input("Enter the path of the folder to review: ")  # Get folder path from user

    # Count only Python files for progress tracking
    total_files = sum(
        [len(files) for _, _, files in os.walk(folder_to_review) if files and any(f.endswith('.py') for f in files)]
    )

    if total_files == 0:
        print("No Python files found for review.")
        return  # Exit if no Python files are found

    print(f"Found {total_files} Python files to review.")
    print("Processing the files... Please wait.")

    # Start timing the review process
    start_time = time.time()

    # Review the files and get the report
    report = review_files(folder_to_review, pylint_options)

    # End timing the review process
    end_time = time.time()
    elapsed_time = end_time - start_time  # Calculate elapsed time

    # Generate a report if there are results
    if report:
        generate_report(report)
        print("Files review completed. Check 'review_report_pylint.md' for details.")
    else:
        print("No Python files found for review.")

    # Print the time taken to complete the process
    print(f"Time taken to complete the review: {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    # Access command-line arguments directly
    pylint_options = sys.argv[1:]  # Get all arguments after the script name
    review(pylint_options)  # Call the review function with any additional options

