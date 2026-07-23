import os
import subprocess
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_tool_installed(tool):
    """Check if the specified tool is installed."""
    try:
        subprocess.run([tool, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        logging.error(f"{tool.capitalize()} is not installed. Please install it using 'pip install {tool}'.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking {tool} version: {e.stderr.decode()}")
        sys.exit(1)

def review_files(folder, tool, tool_options=None):
    report = []
    if not os.path.exists(folder):
        logging.error(f"The folder '{folder}' does not exist.")
        return report

    python_files = [os.path.join(root, f) for root, _, files in os.walk(folder) for f in files if f.endswith('.py')]

    if not python_files:
        print("No Python files found in the specified folder.")
        return report

    for file_path in python_files:
        command = [tool] + (tool_options or []) + [file_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            report.append({
                'file': file_path,
                'type': 'Python',
                'output': result.stdout.strip(),
                'error': result.stderr.strip(),
                'return_code': result.returncode})
        except subprocess.CalledProcessError as e:
            report.append({
                'file': file_path,
                'type': 'Python',
                'output': e.stdout.strip(),
                'error': e.stderr.strip(),
                'return_code': e.returncode})

    return report

def generate_report(report, tool):
    report_filename = f'review_report_{tool}.md'
    with open(report_filename, 'w') as f:
        f.write(f"# {tool.capitalize()} Code Review Report\n\n")
        # Pylint Return Codes Section
        f.write("## Pylint Return Codes:\n")
        f.write("0: No issues found. The code is clean according to the linting rules.\n")
        f.write(
            "1: One or more issues were found. This indicates that there are linting errors or warnings in the code.\n")
        f.write(
            "2: Pylint was unable to check the code due to an error (e.g., a syntax error in the code being analyzed).\n")
        f.write("4: Pylint was unable to find the specified module or file.\n")
        f.write("8: Pylint encountered a fatal error (e.g., an internal error).\n\n")
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

def review(tool, tool_options):
    check_tool_installed(tool)
    folder_to_review = input("Enter the path of the folder to review: ")

    # Count only Python files for progress tracking
    total_files = sum(
        [len(files) for _, _, files in os.walk(folder_to_review) if files and any(f.endswith('.py') for f in files)])

    if total_files == 0:
        print("No Python files found for review.")
        return

    print(f"Found {total_files} Python files to review.")
    print("Processing the files... Please wait.")
    report = review_files(folder_to_review, tool, tool_options)

    if report:
        generate_report(report, tool)
        print(f"Files review completed. Check '{tool}_review_report.md' for details.")
    else:
        print("No Python files found for review.")

def display_menu():
    print("Select a tool to review Python files:")
    print("1. Pylint")
    print("2. Flake8")
    print("3. Black")
    print("4. Mypy")
    print("5. Bandit")
    print("6. Pyflakes")
    print("0. Exit")

def get_tool_choice():
    while True:
        display_menu()
        choice = input("Enter the number of your choice: ")
        if choice == '1':
            return 'pylint'
        elif choice == '2':
            return 'flake8'
        elif choice == '3':
            return 'black'
        elif choice == '4':
            return 'mypy'
        elif choice == '5':
            return 'bandit'
        elif choice == '6':
            return 'pyflakes'
        elif choice == '0':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    tool = get_tool_choice()
    tool_options = input("Enter any additional options for the tool (separated by spaces): ").split()
    review(tool, tool_options)
