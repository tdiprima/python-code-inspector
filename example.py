# Example usage of the code analyzer and test generator
from my_module.code_analyzer import *

# Sample source code to analyze
source_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""

# Analyze code for issues
print("Analyzing code for issues...\n")
issues = analyze_code(source_code)
if issues:
    for issue in issues:
        print(f"Line {issue.line_number}: {issue.description}")
        if issue.optimized_code:
            print(f"Suggested optimization:\n{issue.optimized_code}\n")
else:
    print("No issues detected!\n")

# Generate unit tests
print("Generating unit tests...\n")
module_name = "my_module"
tests = generate_tests(source_code, module_name)

# Output the generated tests
print("\nGenerated tests:")
print(tests)

# Optional: Save the generated tests to a file
test_file_path = "test_my_module.py"
with open(test_file_path, "w") as test_file:
    test_file.write(tests)
print(f"\nUnit tests saved to {test_file_path}")
