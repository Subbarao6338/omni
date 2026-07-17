import ast
import sys
import time
import os
from io import StringIO
from pathlib import Path
from datetime import datetime
from pylint import lint
from pylint.reporters.text import TextReporter


def get_pylint_results(file_path):
    """Runs Pylint on a file and returns the results."""
    start_time = time.time()
    try:
        # Create a StringIO object to capture the output of the linter
        output_buffer = StringIO()
        # Initialize a TextReporter with the output buffer to collect linting results
        reporter = TextReporter(output_buffer)
        # Prepare the arguments for the linter
        # args = [str(file_path), '--rcfile=./Config/.pylintrc']
        args = [str(file_path)]
        # Run the linter with the specified arguments and the custom reporter
        # Setting exit=False prevents the linter from calling sys.exit()
        run = lint.Run(args, reporter=reporter, exit=False)
        # Retrieve the captured output from the StringIO buffer
        output = output_buffer.getvalue()
        # Extract the rating from the output using a generator expression
        rating = next((line.split("rated at ")[1].split("/10")[0] for line in output.splitlines() if
                       "Your code has been rated at" in line), None)
        # Count logical lines of code
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
            "convention_count": len(categorized_issues['Convention']),
            "warning_count": len(categorized_issues['Warning']),
            "error_count": len(categorized_issues['Error']),
            'refactoring_count': len(categorized_issues['Refactoring']),
            'information_count': len(categorized_issues['Information']),
            'undefined_count': len(categorized_issues['Undefined']),
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
                                     ast.ExceptHandler
                                     # ast.Nonlocal, ast.Match, ast.GeneratorExp, ast.BinOp, ast.UnaryOp, ast.BoolOp,
                                     # ast.ListComp, ast.SetComp, ast.DictComp, ast.Call, ast.Attribute, ast.Subscript,
                                     # ast.Compare, ast.IfExp, ast.List, ast.Tuple, ast.Dict, ast.Set,  ast.AnnAssign,
                                     # ast.AugAssign,
                                     )):
                    count += 1
            return count
    except Exception as e:  # Catch other potential errors
        print(f"An error occurred: {e}")
        return 0

def generate_report(pylint_results, output_file, total_review_time):
    """Generates a report based on the Pylint results."""
    # Get the directory path of the output file
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
        file.write("- Other Issues\n")

        file.write("### Coding Standards Adherence\n\n")
        file.write("The code was reviewed against the organization standards. These standards are defined in .pylintrc file.\n")

        file.write("### Pylint Rating Calculation\n")
        file.write(">Default Formula is: max(0, 0 if fatal else min(10, 10.0 - ((5 * error + warning + refactor + convention) / statement * 10)))\n")
        file.write(">\n")
        file.write(">Formula in Pylintrc is: max(0, min(10, 10.0 - ((3 * error + 2 * warning + 1 * refactor + 1 * convention) / statement * 10)))\n")
        file.write("   - Pylint assigns a rating to the analyzed code on a scale from 0 to 10.\n")
        file.write("   - **Statement** is the number of logical lines of code excluding comments, docstrings, blank lines.\n")
        file.write("   - **5, 3, 2, 1** are the weight factors applied to issues.\n")
        file.write("   - **max()** is to ensure that the score never goes below 0.\n")
        file.write(">[!NOTE]\n")
        file.write(">\n")
        file.write(">In this report, logical lines of code are similar to statements in Pylint, but they are not the same. ")
        file.write("Pylint uses its own internal logic for counting statements, which is not publicly documented. ")
        file.write("Therefore, our count may be close to Pylint's, but it may not match exactly.\n")

        # Write report summary
        total_files = len(pylint_results)
        files_with_issues = sum(1 for result in pylint_results.values() if result["exit_code"] != 0)
        total_convention = sum(result["convention_count"] for result in pylint_results.values())
        total_warnings = sum(result["warning_count"] for result in pylint_results.values())
        total_errors = sum(result["error_count"] for result in pylint_results.values())
        total_refactoring = sum(result["refactoring_count"] for result in pylint_results.values())
        total_information = sum(result["information_count"] for result in pylint_results.values())
        total_undefined = sum(result["undefined_count"] for result in pylint_results.values())
        total_loc = sum(result["loc_count"] for result in pylint_results.values())
        total_rating = sum(float(result['rating']) for result in pylint_results.values() if result['rating'] is not None)
        average_rating = total_rating / total_files if total_files > 0 else 0

        file.write("### Summary\n")
        file.write(f"- **Total Files Reviewed:** {total_files}\n")
        file.write(f"- **Files with Issues:** {files_with_issues}\n")
        file.write(f"- **Files without Issues:** {total_files - files_with_issues}\n")
        file.write(f"- **Total Review Time:** {total_review_time:.2f} seconds\n\n")

        # Write overall issues count
        file.write("### Overall Issues Count\n")
        file.write(f"- **Total Convention Issues:** {total_convention}\n")
        file.write(f"- **Total Warning Issues:** {total_warnings}\n")
        file.write(f"- **Total Error Issues:** {total_errors}\n")
        file.write(f"- **Total Refactoring Issues:** {total_refactoring}\n")
        file.write(f"- **Total Information Issues:** {total_information}\n")
        file.write(f"- **Total Other Issues:** {total_undefined}\n")
        file.write(f"- **Total Logical Lines of Code:** {total_loc}\n")
        file.write(f"- **Average Rating:** {average_rating:.2f}/10\n\n")

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
            file.write(f"- **Other Issues Count:** {result['undefined_count']}\n")
            file.write(f"- **Logical Lines of Code:** {result['loc_count']}\n")
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

                # Write Undefined issues if any
                if result.get("undefined_issues"):
                    file.write("#### Other Issues:\n")
                    for issue in result["undefined_issues"]:
                        file.write(f"- {issue}\n")
                    file.write("\n")


def main():
    """Runs the Pylint code review tool."""
    directory_path = input("Enter the directory path to review: ").strip()
    # Check if the provided path is a valid directory
    if not Path(directory_path).is_dir():
        print(f"Error: '{directory_path}' is not a valid directory.")
        sys.exit(1)

    # Find all Python files in the specified directory
    python_files = list(Path(directory_path).rglob("*.py"))
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
        # Get the Pylint results for the current file
        result = get_pylint_results(file_path)
        end_time = time.time()
        total_review_time += end_time - start_time
        if result is not None:
            # Store the Pylint result for the file
            pylint_results[file_path] = result
        else:
            print(f"Skipping file '{file_path}' due to an error during Pylint execution.")

    report_file = "./Reports/pylint_report.md"
    generate_report(pylint_results, report_file, total_review_time)
    print(f"Review completed. Total review time: {total_review_time:.2f} seconds. Report saved to '{os.path.relpath(report_file)}'.")

if __name__ == "__main__":
    main()

