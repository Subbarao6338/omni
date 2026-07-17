import sys
from pylint import lint
from pathlib import Path
from datetime import datetime


def run_pylint(file_path):
    """Run Pylint on a given file and return the output, rating, and exit code."""
    try:
        result = lint.Run([str(file_path)], exit=False)
        output = result.linter.reporter.out.getvalue()
        rating = next(
            (line.split("rated at ")[1].split("/10")[0] for line in output.splitlines() if "Your code has been rated at" in line),
            None
        )
        exit_code = result.linter.stats.global_note
        return output, rating, exit_code
    except Exception as e:
        print(f"Error running pylint on {file_path}: {e}")
        return None, None, None


def generate_report(file_reports, output_file):
    """Generate a Markdown report from the Pylint results."""
    with open(output_file, "w") as md_file:
        md_file.write("# Pylint Code Review Report\n\n")
        md_file.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        md_file.write("## Summary\n\n")

        total_files = len(file_reports)
        files_with_issues = sum(1 for report in file_reports.values() if report["exit_code"] != 0)

        md_file.write(f"- **Total Files Reviewed:** {total_files}\n")
        md_file.write(f"- **Files with Issues:** {files_with_issues}\n")
        md_file.write(f"- **Files without Issues:** {total_files - files_with_issues}\n\n")

        md_file.write("## Detailed Results\n\n")
        for file_path, report in file_reports.items():
            md_file.write(f"### File: `{file_path}`\n\n")
            md_file.write(f"- **Rating:** {report['rating']}/10\n")
            md_file.write(f"- **Exit Code:** {report['exit_code']}\n\n")
            md_file.write("**Status:** " + ("No issues found." if report["exit_code"] == 0 else "Issues found.") + "\n\n")

            if report["exit_code"] != 0:
                md_file.write("#### Output:\n```\n" + report["output"] + "\n```\n\n")


def main():
    """Main function to execute the Pylint review process."""
    directory_path = input("Enter the directory path to review: ").strip()

    if not Path(directory_path).is_dir():
        print(f"Error: '{directory_path}' is not a valid directory.")
        sys.exit(1)

    python_files = list(Path(directory_path).rglob("*.py"))
    if not python_files:
        print("No Python files found in the directory.")
        sys.exit(0)

    print(f"Found {len(python_files)} Python files. Starting review...")

    file_reports = {}
    for file_path in python_files:
        print(f"Reviewing file: {file_path}")
        output, errors, rating, exit_code = run_pylint(file_path)
        if output is not None:
            file_reports[str(file_path)] = {
                "output": output,
                "errors": errors,
                "rating": rating,
                "exit_code": exit_code
            }

    report_file = "pylint_report.md"
    generate_report(file_reports, report_file)
    print(f"Review completed. Report saved to '{report_file}'.")


if __name__ == "__main__":
    main()
