import ast
import sys
import time
import os
from io import StringIO
from pathlib import Path
from datetime import datetime
from pylint import lint
from pylint.reporters.text import TextReporter
import subprocess

def get_pylint_results(file_path):
    """Runs Pylint on a file and returns the results."""
    start_time = time.time()
    try:
        output_buffer = StringIO()
        reporter = TextReporter(output_buffer)
        args = [str(file_path), '--rcfile=./Config/.pylintrc']  # Custom Pylint config
        run = lint.Run(args, reporter=reporter, exit=False)
        output = output_buffer.getvalue()
        rating = next((line.split("rated at ")[1].split("/10")[0] for line in output.splitlines() if
                       "Your code has been rated at" in line), None)
        loc_count = count_logical_lines_of_code(file_path)
        categorized_issues = categorize_issues(output)
        return {
            "output": output,
            "rating": rating,
            "exit_code": 0 if all(len(issues) == 0 for issues in categorized_issues.values()) else 1,
            "convention_issues": categorized_issues['Convention'],
            "warning_issues": categorized_issues['Warning'],
            "error_issues": categorized_issues['Error'],
            "refactoring_issues": categorized_issues['Refactoring'],
            "information_issues": categorized_issues['Information'],
            "undefined_count": len(categorized_issues['Undefined']),
            "loc_count": loc_count,
            "time_taken": time.time() - start_time
        }
    except Exception as e:
        print(f"Error running pylint on {file_path}: {e}")
        return None

def categorize_issues(pylint_output):
    """Categorizes Pylint issues into Convention, Warning, and Error."""
    categorized_issues = {'Convention': [], 'Warning': [], 'Error': [], 'Refactoring': [], 'Information': [], 'Undefined': []}
    for line in pylint_output.splitlines():
        if ':' in line:
            parts = line.split(':')
            if len(parts) > 3:
                issue_code = parts[3].strip()
                if issue_code.startswith('C'):
                    categorized_issues['Convention'].append(line)
                elif issue_code.startswith('W'):
                    categorized_issues['Warning'].append(line)
                elif issue_code.startswith('E'):
                    categorized_issues['Error'].append(line)
                elif issue_code.startswith('R'):
                    categorized_issues['Refactoring'].append(line)
                elif issue_code.startswith('I'):
                    categorized_issues['Information'].append(line)
                else:
                    categorized_issues['Undefined'].append(line)
    return categorized_issues

def count_logical_lines_of_code(file_path):
    """Counts statements in a Python file (Pylint-like)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
            tree = ast.parse(code)
            count = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.Assign, ast.Expr, ast.Return, ast.Raise, ast.Assert, ast.Delete,
                                     ast.Import, ast.ImportFrom, ast.Pass, ast.Break, ast.Continue, ast.Yield,
                                     ast.YieldFrom, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.For,
                                     ast.AsyncFor, ast.While, ast.If, ast.With, ast.AsyncWith, ast.Try, ast.Global,
                                     ast.ExceptHandler)):
                    count += 1
            return count
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

def generate_report(pylint_results, output_file, total_review_time):
    """Generates a report based on the Pylint results."""
    report_dir = Path(output_file).parent
    report_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as file:
        file.write("# Code Review Report\n\n")
        file.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        # Add more report generation logic as needed...

def run_tool(tool, file_path):
    """Runs the selected code analysis tool on the specified file."""
    if tool == "pylint":
        return get_pylint_results(file_path)
    elif tool == "flake8":
        return get_flake8_results(file_path)
    elif tool == "black":
        return get_black_results(file_path)
    elif tool == "mypy":
        return get_mypy_results(file_path)
    elif tool == "bandit":
        return get_bandit_results(file_path)
    elif tool == "ruff":
        return get_ruff_results(file_path)
    elif tool == "pyflakes":
        return get_pyflakes_results(file_path)
    else:
        print(f"Error: Unknown tool '{tool}'")
        return None


def get_flake8_results(file_path):
    """Runs Flake8 on a file and returns the results."""
    try:
        result = subprocess.run(['flake8', str(file_path)], capture_output=True, text=True)
        output = result.stdout
        categorized_issues = categorize_flake8_issues(output)
        return {
            "output": output,
            "rating": None,  # Flake8 does not provide a rating
            "exit_code": result.returncode,
            "convention_issues": categorized_issues['Convention'],
            "warning_issues": categorized_issues['Warning'],
            "error_issues": categorized_issues['Error'],
            "refactoring_issues": [],  # Flake8 does not categorize refactoring issues
            "information_issues": [],  # Flake8 does not categorize information issues
            "convention_count": len(categorized_issues['Convention']),
            "warning_count": len(categorized_issues['Warning']),
            "error_count": len(categorized_issues['Error']),
            'refactoring_count': 0,
            'information_count': 0,
            'undefined_count': 0,
            "loc_count": count_logical_lines_of_code(file_path),
            "time_taken": 0  # Placeholder for time taken
        }
    except Exception as e:
        print(f"Error running flake8 on {file_path}: {e}")
        return None

def categorize_flake8_issues(flake8_output):
    """Categorizes Flake8 issues into Convention, Warning, and Error."""
    categorized_issues = {'Convention': [], 'Warning': [], 'Error': []}
    for line in flake8_output.splitlines():
        if line:
            # Flake8 uses different codes, you can categorize them based on your needs
            if line.startswith('F'):
                categorized_issues['Error'].append(line)
            elif line.startswith('W'):
                categorized_issues['Warning'].append(line)
            else:
                categorized_issues['Convention'].append(line)
    return categorized_issues

def get_mypy_results(file_path):
    """Runs Mypy on a file and returns the results."""
    try:
        result = subprocess.run(['mypy', str(file_path)], capture_output=True, text=True)
        output = result.stdout
        categorized_issues = categorize_mypy_issues(output)
        return {
            "output": output,
            "rating": None,  # Mypy does not provide a rating
            "exit_code": result.returncode,
            "convention_issues": [],  # Mypy does not categorize convention issues
            "warning_issues": [],  # Mypy does not categorize warning issues
            "error_issues": categorized_issues['Error'],
            "refactoring_issues": [],  # Mypy does not categorize refactoring issues
            "information_issues": [],  # Mypy does not categorize information issues
            "convention_count": 0,
            "warning_count": 0,
            "error_count": len(categorized_issues['Error']),
            'refactoring_count': 0,
            'information_count': 0,
            'undefined_count': 0,
            "loc_count": count_logical_lines_of_code(file_path),
            "time_taken": 0  # Placeholder for time taken
        }
    except Exception as e:
        print(f"Error running mypy on {file_path}: {e}")
        return None

def categorize_mypy_issues(mypy_output):
    """Categorizes Mypy issues into Error."""
    categorized_issues = {'Error': []}
    for line in mypy_output.splitlines():
        if line:
            categorized_issues['Error'].append(line)  # Mypy typically reports errors directly
    return categorized_issues

def get_bandit_results(file_path):
    """Runs Bandit on a file and returns the results."""
    try:
        result = subprocess.run(['bandit', '-r', str(file_path)], capture_output=True, text=True)
        output = result.stdout
        categorized_issues = categorize_bandit_issues(output)
        return {
            "output": output,
            "rating": None,  # Bandit does not provide a rating
            "exit_code": result.returncode,
            "convention_issues": [],  # Bandit does not categorize convention issues
            "warning_issues": [],  # Bandit does not categorize warning issues
            "error_issues": categorized_issues['Error'],
            "refactoring_issues": [],  # Bandit does not categorize refactoring issues
            "information_issues": [],  # Bandit does not categorize information issues
            "convention_count": 0,
            "warning_count": 0,
            "error_count": len(categorized_issues['Error']),
            'refactoring_count': 0,
            'information_count': 0,
            'undefined_count': 0,
            "loc_count": count_logical_lines_of_code(file_path),
            "time_taken": 0  # Placeholder for time taken
        }
    except Exception as e:
        print(f"Error running bandit on {file_path}: {e}")
        return None

def categorize_bandit_issues(bandit_output):
    """Categorizes Bandit issues into Error."""
    categorized_issues = {'Error': []}
    for line in bandit_output.splitlines():
        if line and "Issue" in line:  # Adjust this condition based on Bandit's output format
            categorized_issues['Error'].append(line)
    return categorized_issues

def get_ruff_results(file_path):
    """Runs Ruff on a file and returns the results."""
    try:
        result = subprocess.run(['ruff', str(file_path)], capture_output=True, text=True)
        output = result.stdout
        categorized_issues = categorize_ruff_issues(output)
        return {
            "output": output,
            "rating": None,  # Ruff does not provide a rating
            "exit_code": result.returncode,
            "convention_issues": categorized_issues['Convention'],
            "warning_issues": categorized_issues['Warning'],
            "error_issues": categorized_issues['Error'],
            "refactoring_issues": [],  # Ruff does not categorize refactoring issues
            "information_issues": [],  # Ruff does not categorize information issues
            "convention_count": len(categorized_issues['Convention']),
            "warning_count": len(categorized_issues['Warning']),
            "error_count": len(categorized_issues['Error']),
            'refactoring_count': 0,
            'information_count': 0,
            'undefined_count': 0,
            "loc_count": count_logical_lines_of_code(file_path),
            "time_taken": 0  # Placeholder for time taken
        }
    except Exception as e:
        print(f"Error running ruff on {file_path}: {e}")
        return None

def categorize_ruff_issues(ruff_output):
    """Categorizes Ruff issues into Convention, Warning, and Error."""
    categorized_issues = {'Convention': [], 'Warning': [], 'Error': []}
    for line in ruff_output.splitlines():
        if line:
            # Adjust categorization based on Ruff's output format
            if line.startswith('C'):
                categorized_issues['Convention'].append(line)
            elif line.startswith('W'):
                categorized_issues['Warning'].append(line)
            elif line.startswith('E'):
                categorized_issues['Error'].append(line)
    return categorized_issues

def get_pyflakes_results(file_path):
    """Runs Pyflakes on a file and returns the results."""
    try:
        result = subprocess.run(['pyflakes', str(file_path)], capture_output=True, text=True)
        output = result.stdout
        categorized_issues = categorize_pyflakes_issues(output)
        return {
            "output": output,
            "rating": None,  # Pyflakes does not provide a rating
            "exit_code": result.returncode,
            "convention_issues": [],  # Pyflakes does not categorize convention issues
            "warning_issues": [],  # Pyflakes does not categorize warning issues
            "error_issues": categorized_issues['Error'],
            "refactoring_issues": [],  # Pyflakes does not categorize refactoring issues
            "information_issues": [],  # Pyflakes does not categorize information issues
            "convention_count": 0,
            "warning_count": 0,
            "error_count": len(categorized_issues['Error']),
            'refactoring_count': 0,
            'information_count': 0,
            'undefined_count': 0,
            "loc_count": count_logical_lines_of_code(file_path),
            "time_taken": 0  # Placeholder for time taken
        }
    except Exception as e:
        print(f"Error running pyflakes on {file_path}: {e}")
        return None

def categorize_pyflakes_issues(pyflakes_output):
    """Categorizes Pyflakes issues into Error."""
    categorized_issues = {'Error': []}
    for line in pyflakes_output.splitlines():
        if line:
            categorized_issues['Error'].append(line)  # Pyflakes typically reports errors directly
    return categorized_issues


def get_black_results(file_path):
    """Runs Black on a file and returns the results."""
    try:
        result = subprocess.run(['black', '--check', str(file_path)], capture_output=True, text=True)
        return {
            "output": result.stdout,
            "exit_code": result.returncode,
            "time_taken": 0  # Placeholder for time taken
        }
    except Exception as e:
        print(f"Error running black on {file_path}: {e}")
        return None

def main():
    """Runs the code review tool."""
    print("Welcome to the Code Review Tool!")
    print("Select a tool to run:")
    print("1. Pylint")
    print("2. Flake8")
    print("3. Black")
    print("4. Mypy")
    print("5. Bandit")
    print("6. Ruff")
    print("7. Pyflakes")
    print("0. Exit")

    while True:
        choice = input("Enter your choice (0-7): ").strip()
        if choice == "0":
            print("Exiting the tool.")
            break

        tool_map = {
            "1": "pylint",
            "2": "flake8",
            "3": "black",
            "4": "mypy",
            "5": "bandit",
            "6": "ruff",
            "7": "pyflakes"
        }

        tool = tool_map.get(choice)
        if not tool:
            print("Invalid choice. Please try again.")
            continue

        directory_path = input("Enter the directory path to review: ").strip()
        if not Path(directory_path).is_dir():
            print(f"Error: '{directory_path}' is not a valid directory.")
            continue

        python_files = list(Path(directory_path).rglob("*.py"))
        if not python_files:
            print("No Python files found in the directory.")
            continue

        print(f"Found {len(python_files)} Python files. Starting review...")
        tool_results = {}
        total_review_time = 0
        for file_path in python_files:
            print(f"Reviewing file: {file_path}")
            start_time = time.time()
            result = run_tool(tool, file_path)
            end_time = time.time()
            total_review_time += end_time - start_time
            if result is not None:
                tool_results[file_path] = result
            else:
                print(f"Skipping file '{file_path}' due to an error during {tool} execution.")

        report_file = f"./Reports/{tool}_report.md"
        generate_report(tool_results, report_file, total_review_time)
        print(f"Review completed. Total review time: {total_review_time:.2f} seconds. Report saved to '{os.path.relpath(report_file)}'.")

if __name__ == "__main__":
    main()


