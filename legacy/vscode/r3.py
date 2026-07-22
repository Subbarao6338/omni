import os
from pylint.lint import Run


def generate_pylint_report(path):
    report_file = os.path.join(path, "pylint_report.md")

    with open(report_file, "w") as f:
        f.write("# Pylint Report\n\n")
        f.write("This report analyzes Python files within the specified path using Pylint.\n\n")

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    (pylint_stdout, pylint_stderr) = Run([file_path], return_std=True)

                    # Write the file path as a section header
                    f.write(f"## {file_path}\n\n")

                    # Write the Pylint output
                    f.write("### Pylint Output:\n")
                    f.write("```\n")
                    f.write(pylint_stdout.getvalue())
                    f.write("```\n\n")

                    # If there are any errors or warnings, summarize them
                    if pylint_stderr.getvalue():
                        f.write("### Errors and Warnings:\n")
                        f.write("```\n")
                        f.write(pylint_stderr.getvalue())
                        f.write("```\n\n")

        print(f"Pylint report generated successfully: {report_file}")


if __name__ == "__main__":
    path_to_scan = "."  # Replace with the actual path to scan
    generate_pylint_report(path_to_scan)
