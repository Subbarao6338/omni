import argparse
import os
import markdown
from pylint.lint import Run


def find_python_files(directory):
    """Recursively find all Python files in the given directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def generate_report(results, threshold):
    """Generate a Markdown report from pylint results."""
    report_lines = []
    report_lines.append("# Pylint Report\n")
    report_lines.append(f"**Threshold:** {threshold}\n")
    report_lines.append("| File | Score | Issues |\n")
    report_lines.append("|------|-------|--------|\n")

    for file, result in results.items():
        score = result.linter.stats['global_note']
        issues = result.linter.stats['global_errors'] + result.linter.stats['global_warnings']
        report_lines.append(f"| {file} | {score} | {issues} |\n")

    return ''.join(report_lines)


def main():
    parser = argparse.ArgumentParser(prog="LINT")

    parser.add_argument('-p',
                        '--path',
                        help='Path to directory you want to run pylint | '
                             'Default: %(default)s | '
                             'Type: %(type)s ',
                        default='./local_repo',
                        type=str)

    parser.add_argument('-t',
                        '--threshold',
                        help='Score threshold to fail pylint runner | '
                             'Default: %(default)s | '
                             'Type: %(type)s ',
                        default=7,
                        type=float)

    args = parser.parse_args()
    path = str(args.path)
    threshold = float(args.threshold)

    python_files = find_python_files(path)
    results = {}

    for file in python_files:
        result = Run([file])
        results[file] = result

    final_score = sum(result.linter.stats['global_note'] for result in results.values()) / len(results)

    if final_score < threshold:
        raise Exception(f"Final score {final_score} is below the threshold {threshold}.")

    report = generate_report(results, threshold)

    # Save the report to a markdown file
    with open('pylint_report.md', 'w') as report_file:
        report_file.write(report)

    print("Pylint report generated: pylint_report.md")


if __name__ == "__main__":
    main()
