import sys
from pylint import lint
from pylint.reporters.text import TextReporter
from io import StringIO
from pathlib import Path
from datetime import datetime


def run_pylint(file_path):
    try:
        # Create a buffer to capture the output of Pylint
        output_buffer = StringIO()
        reporter = TextReporter(output_buffer)  # Use a text reporter to format the output
        args = [str(file_path)]  # Prepare the file path as an argument for Pylint

        # Run Pylint with the specified arguments and reporter
        run = lint.Run(args, reporter=reporter, exit=False)
        output = output_buffer.getvalue()  # Get the output from the buffer

        # Extract the rating from the output
        rating = next((line.split("rated at ")[1].split("/10")[0] for line in output.splitlines() if "Your code has been rated at" in line), None)

        # Capture errors from the output
        errors = "\n".join(line for line in output.splitlines() if "E:" in line or "W:" in line)

        # Determine the exit code based on the global note from Pylint
        exit_code = 0 if run.linter.stats.global_note == 10.0 else 1

        return output, errors, rating, exit_code
    except Exception as e:
        print(f"Error running pylint on {file_path}: {e}")
        return None, None, None, None


def generate_report(file_reports, output_file):
    with open(output_file, "w") as file:
        file.write("# Pylint Code Review Report\n\n")
        file.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        file.write("### Pylint Exit Codes:\n")
        file.write("- **0**: No issues found.\n")
        file.write("\n- **1**: One or more issues were found.\n")

        file.write("## Summary\n\n")
        total_files = len(file_reports)
        files_with_issues = sum(1 for report in file_reports.values() if report["exit_code"] != 0)
        file.write(f"- **Total Files Reviewed:** {total_files}\n")
        file.write(f"- **Files with Issues:** {files_with_issues}\n")
        file.write(f"- **Files without Issues:** {total_files - files_with_issues}\n\n")

        file.write("## Detailed Results\n\n")
        for file_path, report in file_reports.items():
            file.write(f"### File: `{file_path}`\n\n")
            file.write(f"- **Rating:** {report['rating']}/10\n")
            file.write(f"- **Exit Code:** {report['exit_code']}\n\n")
            file.write("**Status:** " + ("No issues found." if report["exit_code"] == 0 else "Issues found.") + "\n\n")

            if report["exit_code"] != 0:
                # If there are issues, include the output in the report
                file.write("#### Output:\n```\n" + report["output"] + "\n```\n\n")

                # Include errors if any
                if report.get("errors"):
                    file.write("#### Errors:\n```\n" + report["errors"] + "\n```\n\n")


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
    for file_path in python_files:
        print(f"Reviewing file: {file_path}")
        output, errors, rating, exit_code = run_pylint(file_path)  # Run Pylint on the file
        if output is not None:
            # Store the report for the file
            file_reports[str(file_path)] = {
                "output": output,  # Store the Pylint output
                "errors": errors,  # Store any captured errors
                "rating": rating,  # Store the rating from Pylint
                "exit_code": exit_code  # Store the exit code indicating success or failure
            }
        else:
            # Handle the case where output is None
            print(f"Skipping file '{file_path}' due to an error during Pylint execution.")

    report_file = "pylint_report.md"
    generate_report(file_reports, report_file)
    print(f"Review completed. Report saved to '{report_file}'.")

if __name__ == "__main__":
    main()
