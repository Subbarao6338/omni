import os
import subprocess
import sys
import logging
from argparse import ArgumentParser

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_pylint_installed():
    """Check if pylint is installed."""
    try:
        subprocess.run(['pylint', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        logging.error("Pylint is not installed. Please install it using 'pip install pylint'.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking pylint version: {e.stderr.decode()}")
        sys.exit(1)


def review_files(folder, pylint_options=None):
    report = []
    if not os.path.exists(folder):
        logging.error(f"The folder '{folder}' does not exist.")
        return report

    python_files = [os.path.join(root, f) for root, _, files in os.walk(folder) for f in files if f.endswith('.py')]

    if not python_files:
        print("No Python files found in the specified folder.")
        return report

    for file_path in python_files:
        command = ['pylint'] + (pylint_options or []) + [file_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            report.append({
                'file': file_path,
                'type': 'Python',
                'output': result.stdout.strip(),
                'error': result.stderr.strip(),
                'return_code': result.returncode
            })
        except subprocess.CalledProcessError as e:
            report.append({
                'file': file_path,
                'type': 'Python',
                'output': e.stdout.strip(),
                'error': e.stderr.strip(),
                'return_code': e.returncode
            })

    return report


def generate_report(report):
    with open('review_report_pylint.md', 'w') as f:
        f.write("# Pylint Review Report\n\n")

        # Pylint Return Codes Section
        f.write("## Pylint Return Codes:\n")
        f.write("0: No issues found. The code is clean according to the linting rules.\n")
        f.write(
            "1: One or more issues were found. This indicates that there are linting errors or warnings in the code.\n")
        f.write(
            "2: Pylint was unable to check the code due to an error (e.g., a syntax error in the code being analyzed).\n")
        f.write("4: Pylint was unable to find the specified module or file.\n")
        f.write("8: Pylint encountered a fatal error (e.g., an internal error).\n\n")

        total_messages = 0
        message_counts = {
            'convention': 0,
            'refactor': 0,
            'warning': 0,
            'error': 0
        }
        overall_score = 10.0  # Start with a perfect score

        for entry in report:
            f.write(f"### File: {entry['file']}\n")
            f.write(f"**Type:** {entry['type']}\n")
            f.write("### Output:\n```\n")
            f.write(entry['output'] or "No issues found.\n")
            f.write("\n```\n### Errors:\n```\n")
            f.write(entry['error'] or "No errors.\n")
            f.write("\n```\n### Return Code:\n```\n")
            f.write(str(entry['return_code']) or "N/A.\n")
            f.write("\n```\n\n---\n\n")

            # Analyze output for message counts and score
            if entry['output']:
                for line in entry['output'].splitlines():
                    if line.startswith('C'):
                        message_counts['convention'] += 1
                    elif line.startswith('R'):
                        message_counts['refactor'] += 1
                    elif line.startswith('W'):
                        message_counts['warning'] += 1
                    elif line.startswith('E'):
                        message_counts['error'] += 1

                total_messages += sum(message_counts.values())

        # Calculate overall score based on the number of issues
        overall_score -= (total_messages * 0.1)  # Deduct points for each issue found
        overall_score = max(0, overall_score)  # Ensure score doesn't go below 0

        # Write summary
        f.write("## Summary\n")
        f.write(f"**Total Messages:** {total_messages}\n")
        f.write(f"**Convention Messages:** {message_counts['convention']}\n")
        f.write(f"**Refactor Messages:** {message_counts['refactor']}\n")
        f.write(f"**Warning Messages:** {message_counts['warning']}\n")
        f.write(f"**Error Messages:** {message_counts['error']}\n")
        f.write(f"**Overall Score:** {overall_score:.2f}/10\n")

def review(pylint_options):
    check_pylint_installed()
    folder_to_review = input("Enter the path of the folder to review: ")

    # Count only Python files for progress tracking
    total_files = sum(
        [len(files) for _, _, files in os.walk(folder_to_review) if files and any(f.endswith('.py') for f in files)]
    )

    if total_files == 0:
        print("No Python files found for review.")
        return

    print(f"Found {total_files} Python files to review.")
    print("Processing the files... Please wait.")
    report = review_files(folder_to_review, pylint_options)

    if report:
        generate_report(report)
        print("Files review completed. Check 'review_report_pylint.md' for details.")
    else:
        print("No Python files found for review.")

if __name__ == "__main__":
    parser = ArgumentParser(description="Review Python files using pylint.")
    parser.add_argument('--pylint-options', nargs='*', help='Additional options to pass to pylint.')
    args = parser.parse_args()
    review(args.pylint_options)
