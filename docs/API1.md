# API Documentation

## Project Analysis

### ProjectAnalyzer

```python
from pyrefactor.file_analyzer import ProjectAnalyzer

analyzer = ProjectAnalyzer(
    root_path: str,
    exclude_dirs: List[str] = None,
    exclude_files: List[str] = None
)
```

Creates a new analyzer for Python files.

**Parameters:**

- `root_path` (str): Directory path to analyze
- `exclude_dirs` (List[str], optional): Directories to skip (defaults to ['venv', '.git', '__pycache__', 'build', 'dist'])
- `exclude_files` (List[str], optional): Specific files to skip

**Methods:**

#### analyze_project

```python
def analyze_project(self) -> Dict[str, FileAnalysis]
```

Analyzes all Python files in the specified directory.

**Returns:**

- Dictionary mapping file paths to their analysis results

**Example:**

```python
analyzer = ProjectAnalyzer("./my_project")
results = analyzer.analyze_project()
```

### generate_report

```python
def generate_report(
    self,
    results: Dict[str, FileAnalysis],
    output_file: str = None
) -> str
```

Generates a markdown report of the analysis results.

**Parameters:**

- `results`: Analysis results from analyze_project()
- `output_file` (optional): Path to save the report. If None, returns the report as a string.

**Returns:**

- Generated report as a string

**Example:**

```python
analyzer.generate_report(results, "analysis_report.md")
```

## Analysis Results

### FileAnalysis

```python
@dataclass
class FileAnalysis:
    filepath: Path
    issues: List[CodeIssue]
    error: Optional[str] = None
```

Represents the analysis results for a single file.

**Attributes:**

- `filepath`: Path to the analyzed file
- `issues`: List of detected issues
- `error`: Error message if analysis failed

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
- `issue_type`: Type of the issue (see below)
- `description`: Detailed description of the issue
- `suggestion`: Suggested improvement
- `original_code`: The problematic code snippet
- `optimized_code`: Suggested optimized code (if available)

## Issue Types

The analyzer detects several types of issues:

1. **Complex Functions** (`high_complexity`)
   - Functions with too many decision paths (if statements, loops, etc.)
   - Suggestion to break down into smaller functions

2. **Nested Loops** (`nested_loops`)
   - Loops nested more than 2 levels deep
   - Suggestion to restructure the code

3. **List Comprehension Opportunity** (`list_comprehension`)
   - Loops that could be replaced with list comprehensions
   - Provides optimized list comprehension code

## Best Practices

When using the analyzer:

1. **Project Structure**
   - Organize your Python files in a clear directory structure
   - Use consistent file naming
   - Keep related files together

2. **Excluding Files/Directories**
   - Always exclude virtual environments
   - Consider excluding test files if you only want to analyze production code
   - Exclude generated files

3. **Report Analysis**
   - Review each suggestion in context
   - Consider the impact of suggested changes
   - Test thoroughly after making changes

4. **Common Configurations**

```python
# Basic Python package
analyzer = ProjectAnalyzer(
    root_path="./",
    exclude_dirs=['venv', 'tests', 'docs', 'examples'],
    exclude_files=['setup.py', 'conftest.py']
)
```

<br>
