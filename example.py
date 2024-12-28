# Example usage of the code analyzer and test generator
from code_analyzer import *

# Example usage
source_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""

# Analyze code for issues
issues = analyze_code(source_code)
for issue in issues:
    print(f"Line {issue.line_number}: {issue.description}")
    if issue.optimized_code:
        print(f"Suggested optimization:\n{issue.optimized_code}")

# Generate unit tests
tests = generate_tests(source_code, "my_module")
print("\nGenerated tests:\n", tests)
