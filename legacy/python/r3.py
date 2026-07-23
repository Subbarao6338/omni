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

    # Adjust the file extension for the programming language you want to review
    file_extension = '.py'  # Change this for other languages
    programming_files = [os.path.join(root, f) for root, _, files in os.walk(folder) for f in files if f.endswith(file_extension)]

    if not programming_files:
        print(f"No {file_extension} files found in the specified folder.")
        return report

    for file_path in programming_files:
        command = [tool] + (tool_options or []) + [file_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            report.append({
                'file': file_path,
                'type': 'Programming',
                'output': result.stdout.strip(),
                'error': result.stderr.strip(),
                'return_code': result.returncode})
        except subprocess.CalledProcessError as e:
            report.append({
                'file': file_path,
                'type': 'Programming',
                'output': e.stdout.strip(),
                'error': e.stderr.strip(),
                'return_code': e.returncode})

    return report

def generate_report(report, tool):
    report_filename = f'review_report_{tool}.md'
    with open(report_filename, 'w') as f:
        f.write(f"# {tool.capitalize()} Code Review Report\n\n")
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

    # Count only programming files for progress tracking
    total_files = sum(
        [len(files) for _, _, files in os.walk(folder_to_review) if files and any(f.endswith('.py') for f in files)])

    if total_files == 0:
        print("No programming files found for review.")
        return

    print(f"Found {total_files} programming files to review.")
    print("Processing the files... Please wait.")
    report = review_files(folder_to_review, tool, tool_options)

    if report:
        generate_report(report, tool)
        print(f"Files review completed. Check '{tool}_review_report.md' for details.")
    else:
        print("No programming files found for review.")

def display_menu():
    print("Select a tool to review programming files:")
    print("1. Pylint")
    print("2. Flake8")
    print("3. Black")
    print("4. Mypy")
    print("5. Bandit")
    print("6. Pyflakes")
    print("7. Ruff")
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
        elif choice == '7':
            return 'ruff'
        elif choice == '0':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    tool = get_tool_choice()
    tool_options = input("Enter any additional options for the tool (separated by spaces): ").split()

    # Check for custom configuration files for specific tools
    if tool == 'pylint':
        tool_options.append('--rcfile=./Config/.pylintrc')  # Example for Pylint
    elif tool == 'flake8':
        tool_options.append('--config=./Config/.flake8')  # Example for Flake8
    elif tool == 'black':
        tool_options.append('--config=./Config/pyproject.toml')  # Example for Black
    elif tool == 'mypy':
        tool_options.append('--config-file=./Config/mypy.ini')  # Example for Mypy
    elif tool == 'bandit':
        tool_options.append('--configfile=./Config/bandit.yaml')  # Example for Bandit
    elif tool == 'ruff':
        tool_options.append('--config=./Config/ruff.toml')  # Example for Ruff
    elif tool == 'pyflakes':
        # Pyflakes does not have a config file, but you can add options if needed
        pass

    review(tool, tool_options)

