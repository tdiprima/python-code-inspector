"""
Basic usage examples for the pyrefactor-ai package.
"""
import sys
from pathlib import Path

# Add src directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

# Now we can import from pyrefactor
from pyrefactor import analyze_code, generate_tests


def main():
    # Example 1: Analyzing a simple function with nested loops
    print("Example 1: Analyzing code with nested loops")
    source_code_1 = """
def process_matrix(matrix):
    result = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            for k in range(len(matrix[i][j])):
                result.append(matrix[i][j][k])
    return result
"""
    issues = analyze_code(source_code_1)
    print("\nFound issues:")
    for issue in issues:
        print(f"\nLine {issue.line_number}: {issue.issue_type}")
        print(f"Description: {issue.description}")
        print(f"Suggestion: {issue.suggestion}")
        if issue.optimized_code:
            print(f"Optimized code:\n{issue.optimized_code}")

    # Example 2: Analyzing a function that could use list comprehension
    print("\nExample 2: Analyzing code with potential list comprehension")
    source_code_2 = """
def get_squares(numbers):
    squares = []
    for num in numbers:
        squares.append(num * num)
    return squares
"""
    issues = analyze_code(source_code_2)
    print("\nFound issues:")
    for issue in issues:
        print(f"\nLine {issue.line_number}: {issue.issue_type}")
        print(f"Description: {issue.description}")
        print(f"Suggestion: {issue.suggestion}")
        if issue.optimized_code:
            print(f"Optimized code:\n{issue.optimized_code}")

    # Example 3: Generating unit tests
    print("\nExample 3: Generating unit tests")
    source_code_3 = """
def calculate_statistics(numbers):
    if not numbers:
        return None
    total = sum(numbers)
    mean = total / len(numbers)
    squared_diff_sum = sum((x - mean) ** 2 for x in numbers)
    variance = squared_diff_sum / len(numbers)
    return {
        'mean': mean,
        'variance': variance,
        'std_dev': variance ** 0.5
    }
"""
    tests = generate_tests(source_code_3, "stats_module")
    print("\nGenerated test code:")
    print(tests)


if __name__ == "__main__":
    main()
