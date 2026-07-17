import sys
from pylint import lint
from pylint.reporters.text import TextReporter
from io import StringIO
from pathlib import Path
from datetime import datetime
import time
import os

def get_pylint_results(file_path: str) -> dict:
    """Runs Pylint on a file and returns the results."""
    start_time = time.time()
    try:
        output_buffer = StringIO()
        reporter = TextReporter(output_buffer)
        # args = [file_path, '--rcfile=../Config/.pylintrc']
        script_dir = os.path.dirname(os.path.abspath(__file__))
        rcfile_path = os.path.abspath(os.path.join(script_dir, '../Config', '.pylintrc'))
        args = [str(file_path), f'--rcfile={rcfile_path}']
        # args = [str(file_path)]
        run = lint.Run(args, reporter=reporter, exit=False)
        output = output_buffer.getvalue()

        rating = next((line.split("rated at ")[1].split("/10")[0] for line in output.splitlines() if
                       "Your code has been rated at" in line), None)
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
            "convention_count": len(categorized_issues['Convention']),
            "warning_count": len(categorized_issues['Warning']),
            "error_count": len(categorized_issues['Error']),
            'refactoring_count': len(categorized_issues['Refactoring']),
            'information_count': len(categorized_issues['Information']),
            "time_taken": time.time() - start_time
        }
    except Exception as e:
        print(f"Error running pylint on {file_path}: {e}")
        return None


def categorize_issues(pylint_output: str) -> dict:
    """Categorizes Pylint issues into Convention, Warning, and Error."""
    categorized_issues = {'Convention': [], 'Warning': [], 'Error': [], 'Refactoring': [], 'Information': []}
    for line in pylint_output.splitlines():
        # print(line)
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
    # print(categorized_issues)
    return categorized_issues


def generate_report(pylint_results: dict, output_file: str, total_review_time: float) -> None:
    """Generates a report based on the Pylint results."""
    report_dir = Path(output_file).parent
    report_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as file:
        # Write report header
        file.write("# Pylint Code Review Report\n\n")
        file.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        file.write("### Pylint Exit Codes:\n")
        file.write("- **0**: No issues found.\n")
        file.write("- **1**: One or more issues were found.\n\n")

        file.write("### Pylint categories of issues:\n")
        file.write("- **C**: Convention (related to coding style)\n")
        file.write("- **W**: Warning (potential issues that may not necessarily be errors)\n")
        file.write("- **E**: Error (actual errors in the code)\n")
        file.write("- **R**: Refactoring issues (e.g., suggestions for improving code structure and organization)\n")
        file.write("- **I**: Informational messages (e.g., notes about the code, suggestions for improvement)\n")

        file.write("### Coding Standards Adherence\n\n")
        file.write("The code was reviewed against the following standards:\n")
        file.write("- Maximum line length: 100 characters\n")
        file.write("- Docstrings are required (disabled check for missing docstrings)\n\n")

        file.write("### Pylint Rating Calculation\n")
        file.write("Pylint assigns a rating to the analyzed code on a scale from 0 to 10, where:\n")
        file.write("- **10**: Perfect code with no issues.\n")
        file.write("- **Lower scores**: Indicate the presence of various issues.\n\n")
        file.write("**Calculation Process**:\n")
        file.write("   - Start with a score of **10**.\n")
        file.write("   - Deduct points for each issue found. Deduct **0.5** points for each Convention issue, **1** point for each Warning, **2** points for each Error, **0.5** points for each Refactoring issue, and **0** points for each Informational Messsage.\n")
        file.write("   - The final score is capped at a minimum of **0**.\n\n")
        # Write report summary
        total_files = len(pylint_results)
        files_with_issues = sum(1 for result in pylint_results.values() if result["exit_code"] != 0)
        total_convention = sum(result["convention_count"] for result in pylint_results.values())
        total_warnings = sum(result["warning_count"] for result in pylint_results.values())
        total_errors = sum(result["error_count"] for result in pylint_results.values())
        total_refactoring = sum(result["refactoring_count"] for result in pylint_results.values())
        total_information = sum(result["information_count"] for result in pylint_results.values())

        file.write("### Summary\n\n")
        file.write(f"- **Total Files Reviewed:** {total_files}\n")
        file.write(f"- **Files with Issues:** {files_with_issues}\n")
        file.write(f"- **Files without Issues:** {total_files - files_with_issues}\n\n")
        file.write(f"- **Total Review Time:** {total_review_time:.2f} seconds\n\n")

        # Write overall issues count
        file.write("### Overall Issues Count\n")
        file.write(f"- **Total Convention Issues:** {total_convention}\n")
        file.write(f"- **Total Warning Issues:** {total_warnings}\n")
        file.write(f"- **Total Error Issues:** {total_errors}\n\n")
        file.write(f"- **Total Refactoring Issues:** {total_refactoring}\n\n")
        file.write(f"- **Total Information Issues:** {total_information}\n\n")

        # Write detailed results
        file.write("## Detailed Results\n\n")
        for file_path, result in pylint_results.items():
            file.write(f"### File: `{file_path}`\n\n")
            file.write(f"- **Rating:** {result['rating']}/10\n")
            file.write("- **Status:** " + ("No issues found." if result["exit_code"] == 0 else "Issues found.") + "\n")
            file.write(f"- **Exit Code:** {result['exit_code']}\n")
            file.write(f"- **Convention Issues Count:** {result['convention_count']}\n")
            file.write(f"- **Warning Issues Count:** {result['warning_count']}\n")
            file.write(f"- **Error Issues Count:** {result['error_count']}\n")
            file.write(f"- **Refactoring Issues Count:** {result['refactoring_count']}\n")
            file.write(f"- **Information Issues Count:** {result['information_count']}\n")
            file.write(f"- **Review Time:** {result['time_taken']:.2f} seconds\n\n")

            if result["exit_code"] != 0:
                # Write output if there are issues
                file.write("#### Output:\n```\n" + result["output"] + "\n```\n\n")
                # Write convention issues if any
                if result.get("convention_issues"):
                    file.write("#### Convention Issues:\n")
                    for issue in result["convention_issues"]:
                        file.write(f"- {issue}\n")
                    file.write("\n")

                # Write warning issues if any
                if result.get("warning_issues"):
                    file.write("#### Warning Issues:\n")
                    for issue in result["warning_issues"]:
                        file.write(f"- {issue}\n")
                    file.write("\n")

                # Write error issues if any
                if result.get("error_issues"):
                    file.write("#### Error Issues:\n")
                    for issue in result["error_issues"]:
                        file.write(f"- {issue}\n")
                    file.write("\n")

                # Write Refactoring issues if any
                if result.get("refactoring_issues"):
                    file.write("#### Refactoring Issues:\n")
                    for issue in result["refactoring_issues"]:
                        file.write(f"- {issue}\n")
                    file.write("\n")

                # Write Information issues if any
                if result.get("information_issues"):
                    file.write("#### Information Issues:\n")
                    for issue in result["information_issues"]:
                        file.write(f"- {issue}\n")
                    file.write("\n")


def main() -> None:
    """Runs the Pylint code review tool."""
    directory_path = input("Enter the directory path to review: ")
    # directory_path = Path(input("Enter the directory path to review: ").strip()).resolve()
    # directory_path = os.path.abspath(directory_path)
    if not Path(directory_path).is_dir():
        print(f"Error: '{directory_path}' is not a valid directory.")
        sys.exit(1)

    # Find all Python files in the specified directory
    # python_files = [os.path.join(root, f) for root, _, files in os.walk(directory_path) for f in files if f.endswith('.py')]
    python_files = list(Path(directory_path).rglob("*.py"))
    # python_files = [str(file) for file in Path(directory_path).rglob("*.py")]
    # python_files = [files for _, _, files in os.walk(directory_path) if files and any(f.endswith('.py') for f in files)]
    if not python_files:
        print("No Python files found in the directory.")
        sys.exit(0)

    print(f"Found {len(python_files)} Python files. Starting review...")
    # Dictionary to store Pylint results for each file
    pylint_results = {}
    total_review_time = 0
    for file_path in python_files:
        print(f"Reviewing file: {file_path}")
        start_time = time.time()
        result = get_pylint_results(file_path)
        end_time = time.time()
        total_review_time += end_time - start_time
        if result is not None:
            # Store the Pylint result for the file
            pylint_results[file_path] = result
        else:
            print(f"Skipping file '{file_path}' due to an error during Pylint execution.")

    # report_file = "../Reports/pylint_report.md"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_file = os.path.join(script_dir, '../Reports', 'pylint_report.md')

    generate_report(pylint_results, report_file, total_review_time)
    print(f"Review completed. Total review time: {total_review_time:.2f} seconds. Report saved to '{os.path.relpath(report_file)}'.")

if __name__ == "__main__":
    main()

