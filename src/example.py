from pyrefactor import analyze_code, generate_tests

source_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""

# Analyze code
issues = analyze_code(source_code)

# Generate tests
tests = generate_tests(source_code, "my_module")
