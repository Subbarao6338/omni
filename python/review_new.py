import sys
from pylint import lint
from pylint.reporters.text import TextReporter
from io import StringIO
from pathlib import Path
from datetime import datetime
import time

def categorize_issues(pylint_output):
    categorized_issues = {
        'Convention': [],
        'Warning': [],
        'Error': []
    }

    for line in pylint_output.splitlines():
        if ':' in line:
            parts = line.split(':')
            if len(parts) > 4:
                issue_code = parts[4].strip()
                # Categorize based on the issue code prefix
                if issue_code.startswith('C'):
                    categorized_issues['Convention'].append(line)
                elif issue_code.startswith('W'):
                    categorized_issues['Warning'].append(line)
                elif issue_code.startswith('E'):
                    categorized_issues['Error'].append(line)

    return categorized_issues

def run_pylint(file_path):
    start_time = time.time()
    try:
        output_buffer = StringIO()
        reporter = TextReporter(output_buffer)
        args = [str(file_path), '--rcfile=../Config/.pylintrc']  # Include the rcfile argument

        run = lint.Run(args, reporter=reporter, exit=False)
        output = output_buffer.getvalue()
        rating = next((line.split("rated at ")[1].split("/10")[0] for line in output.splitlines() if "Your code has been rated at" in line), None)
        categorized_issues = categorize_issues(output)

        convention_count = len(categorized_issues['Convention'])
        warning_count = len(categorized_issues['Warning'])
        error_count = len(categorized_issues['Error'])

        # Determine exit code based on the presence of issues
        exit_code = 0 if (convention_count == 0 and warning_count == 0 and error_count == 0) else 1
        time_taken = time.time() - start_time
        return output, rating, exit_code, categorized_issues['Convention'], categorized_issues['Warning'], categorized_issues['Error'], convention_count, warning_count, error_count, time_taken
    except Exception as e:
        print(f"Error running pylint on {file_path}: {e}")
        return None, None, None, [], [], [], 0, 0, 0, 0

def generate_report(file_reports, output_file, total_review_time):
    # Ensure the directory for the report exists
    report_dir = Path(output_file).parent
    report_dir.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as file:
        file.write("# Pylint Code Review Report\n\n")
        file.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        file.write("### Pylint Exit Codes:\n")
        file.write("- **0**: No issues found.\n")
        file.write("- **1**: One or more issues were found.\n\n")

        file.write("### Pylint categories of issues:\n")
        file.write("- **C**: Convention (related to coding style)\n")
        file.write("- **W**: Warning (potential issues that may not necessarily be errors)\n")
        file.write("- **E**: Error (actual errors in the code)\n")

        file.write("### Coding Standards Adherence\n\n")
        file.write("The code was reviewed against the following standards:\n")
        file.write("- Maximum line length: 100 characters\n")
        file.write("- Docstrings are required (disabled check for missing docstrings)\n\n")

        file.write("### Pylint Rating Calculation\n")
        file.write("Pylint assigns a rating to the analyzed code on a scale from 0 to 10, where:\n")
        file.write("- **10**: Perfect code with no issues.\n")
        file.write("- **Lower scores**: Indicate the presence of various issues.\n\n")
        file.write("**How the Rating is Calculated:**\n")
        file.write("1. **Issue Severity**:\n")
        file.write("   - **Convention (C)**: Style-related issues (e.g., naming conventions).\n")
        file.write("   - **Warning (W)**: Potential issues that may not be errors (e.g., unused variables).\n")
        file.write("   - **Error (E)**: Actual errors that prevent code execution (e.g., syntax errors).\n\n")

        file.write("2. **Weighting of Issues**:\n")
        file.write("   - Each type of issue has a different impact on the score:\n")
        file.write("     - Errors typically have a higher negative impact than warnings or conventions.\n\n")

        file.write("3. **Calculation Process**:\n")
        file.write("   - Start with a score of **10**.\n")
        file.write("   - Deduct points for each issue found:\n")
        file.write("   - Example: Deduct **0.5** points for each Convention issue, **1** point for each Warning, and **2** points for each Error.\n")
        file.write("   - The final score is capped at a minimum of **0**.\n\n")

        total_files = len(file_reports)
        files_with_issues = sum(1 for report in file_reports.values() if report["exit_code"] != 0)
        total_convention = sum(report["convention_count"] for report in file_reports.values())
        total_warnings = sum(report["warning_count"] for report in file_reports.values())
        total_errors = sum(report["error_count"] for report in file_reports.values())

        file.write("### Summary\n\n")
        file.write(f"- **Total Files Reviewed:** {total_files}\n")
        file.write(f"- **Files with Issues:** {files_with_issues}\n")
        file.write(f"- **Files without Issues:** {total_files - files_with_issues}\n\n")
        file.write(f"- **Total Review Time:** {total_review_time:.2f} seconds\n\n")

        file.write("### Overall Issues Count\n")
        file.write(f"- **Total Convention Issues:** {total_convention}\n")
        file.write(f"- **Total Warning Issues:** {total_warnings}\n")
        file.write(f"- **Total Error Issues:** {total_errors}\n\n")

        file.write("## Detailed Results\n\n")
        for file_path, report in file_reports.items():
            file.write(f"### File: `{file_path}`\n\n")
            file.write(f"- **Rating:** {report['rating']}/10\n")
            file.write("- **Status:** " + ("No issues found." if report["exit_code"] == 0 else "Issues found.") + "\n")
            file.write(f"- **Exit Code:** {report['exit_code']}\n")
            file.write(f"- **Convention Issues Count:** {report['convention_count']}\n")
            file.write(f"- **Warning Issues Count:** {report['warning_count']}\n")
            file.write(f"- **Error Issues Count:** {report['error_count']}\n")
            file.write(f"- **Review Time:** {report['time_taken']:.2f} seconds\n\n")

            if report["exit_code"] != 0:
                # If there are issues, include the output in the report
                file.write("#### Output:\n```\n" + report["output"] + "\n```\n\n")

                # Include convention issues if any
                if report.get("convention_issues"):
                    file.write("#### Convention Issues:\n")
                    for issue in report["convention_issues"]:
                        file.write(f"- {issue}\n")
                    file.write("\n")

                # Include warning issues if any
                if report.get("warning_issues"):
                    file.write("#### Warning Issues:\n")
                    for issue in report["warning_issues"]:
                        file.write(f"- {issue}\n")
                    file.write("\n")

                # Include error issues if any
                if report.get("error_issues"):
                    file.write("#### Error Issues:\n")
                    for issue in report["error_issues"]:
                        file.write(f"- {issue}\n")
                    file.write("\n")

def main():
    directory_path = input("Enter the directory path to review: ").strip()
    if not Path(directory_path).is_dir():
        print(f"Error: '{directory_path}' is not a valid directory.")
        sys.exit(1)

    # Find all Python files in the specified directory
    python_files = list(Path(directory_path).rglob("*.py"))
    if not python_files:
        print("No Python files found in the directory.")
        sys.exit(0)

    print(f"Found {len(python_files)} Python files. Starting review...")

    file_reports = {}  # Dictionary to store reports for each file
    total_review_time = 0
    for file_path in python_files:
        print(f"Reviewing file: {file_path}")
        output, rating, exit_code, convention_issues, warning_issues, error_issues, convention_count, warning_count, error_count, time_taken = run_pylint(file_path)
        total_review_time += time_taken
        if output is not None:
            # Store the report for the file
            file_reports[str(file_path)] = {
                "output": output,
                "rating": rating,
                "exit_code": exit_code,
                "convention_issues": convention_issues,
                "warning_issues": warning_issues,
                "error_issues": error_issues,
                "convention_count": convention_count,
                "warning_count": warning_count,
                "error_count": error_count,
                "time_taken": time_taken
            }
        else:
            print(f"Skipping file '{file_path}' due to an error during Pylint execution.")

    report_file = "../Reports/pylint_report.md"
    generate_report(file_reports, report_file, total_review_time)
    print(f"Review completed. Total review time: {total_review_time:.2f} seconds. Report saved to '{report_file}'.")

if __name__ == "__main__":
    main()
