import os

def calculate_scores(file_path, keywords):
    """
    Calculate the total score and individual keyword scores for a given file.
    """
    total_score = 0
    keyword_scores = {keyword: 0 for keyword in keywords}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                for keyword in keywords:
                    if keyword.lower() in line.lower():
                        total_score += 1
                        keyword_scores[keyword] += 1
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return total_score, keyword_scores


def keyword_score():
    directory_path = input("Enter the directory path: ")

    if not os.path.isdir(directory_path):
        print("Invalid directory path. Please check and try again.")
        return  # Exit the program if the directory is invalid

    keywords = [keyword.strip() for keyword in input("Enter the keywords (comma-separated): ").split(',')]

    scores = {}

    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            total_score, keyword_scores = calculate_scores(file_path, keywords)
            scores[file] = (total_score, keyword_scores)

    # Sort files by total score
    for file, (total_score, keyword_scores) in sorted(scores.items(), key=lambda x: x[1][0], reverse=True):
        print(f"\n{file}:")
        print(f"  Total score: {total_score}")
        for keyword, keyword_score in keyword_scores.items():
            print(f"  {keyword}: {keyword_score}")


if __name__ == "__main__":
    keyword_score()
