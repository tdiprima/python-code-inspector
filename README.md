# Python Code Inspector

![License](https://img.shields.io/github/license/tdiprima/GroqLab-AI)
![Languages](https://img.shields.io/github/languages/top/tdiprima/GroqLab-AI)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)

A Python code refactoring and optimization assistant that analyzes codebases, identifies inefficiencies, and suggests improvements.

## Features

- 🔍 Static code analysis for common inefficiencies
- 🤖 AI-driven code refactoring suggestions
- 🦨 Code smell detection
- ⚡ Performance optimization recommendations
- 🧪 Automatic unit test generation

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from pyrefactor import analyze_code, generate_tests

# Analyze your code
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

# Generate unit tests
tests = generate_tests(source_code, "my_module")
```

## Requirements

- Python 3.8+
- ast (standard library)
- astroid
- pylint
- radon

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<br>
