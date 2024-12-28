# API Documentation

## Core Functions

### analyze_code

```python
def analyze_code(source_code: str) -> List[CodeIssue]
```

Analyzes Python source code for potential improvements and issues.

**Parameters:**

- `source_code` (str): The Python source code to analyze

**Returns:**

- List[CodeIssue]: A list of detected code issues with suggestions

**Example:**

```python
from pyrefactor_ai import analyze_code

source_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""

issues = analyze_code(source_code)
for issue in issues:
    print(f"Line {issue.line_number}: {issue.description}")
```

### generate_tests

```python
def generate_tests(source_code: str, module_name: str) -> str
```

Generates unit tests for the provided source code.

**Parameters:**

- `source_code` (str): The Python source code to generate tests for
- `module_name` (str): The name of the module being tested

**Returns:**

- str: Generated unit test code

**Example:**

```python
from pyrefactor_ai import generate_tests

tests = generate_tests(source_code, "my_module")
print(tests)
```

## Models

### CodeIssue

```python
@dataclass
class CodeIssue:
    line_number: int
    issue_type: str
    description: str
    suggestion: str
    original_code: str
    optimized_code: str = None
```

Represents a detected code issue with suggested improvements.

**Attributes:**

- `line_number`: Line number where the issue was found
- `issue_type`: Type of the issue (e.g., "high_complexity", "nested_loops")
- `description`: Detailed description of the issue
- `suggestion`: Suggested improvement
- `original_code`: The problematic code snippet
- `optimized_code`: Suggested optimized code (if available)

## Issue Types

The analyzer detects several types of issues:

1. **High Complexity** (`high_complexity`)
   - Functions with high cyclomatic complexity (>10)
   - Suggestion to break down into smaller functions

2. **Nested Loops** (`nested_loops`)
   - Deeply nested loops (>2 levels)
   - Suggestion to restructure the code

3. **List Comprehension Opportunity** (`list_comprehension`)
   - Loops that could be replaced with list comprehensions
   - Provides optimized list comprehension code

## Best Practices

When using the analyzer:

1. **Code Preparation**
   - Ensure your code is syntactically correct
   - Use consistent formatting
   - Remove unused imports and variables

2. **Analysis Results**
   - Review each suggestion carefully
   - Consider the context before applying changes
   - Test thoroughly after refactoring

3. **Test Generation**
   - Review and customize generated tests
   - Add specific test cases
   - Include edge cases and error conditions

<br>
