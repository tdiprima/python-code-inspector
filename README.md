# Python Code Inspector

![License](https://img.shields.io/github/license/tdiprima/GroqLab-AI)
![Languages](https://img.shields.io/github/languages/top/tdiprima/GroqLab-AI)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)

A refactoring and optimization assistant that analyzes codebases, identifies inefficiencies, and suggests improvements.

## Code Quality Checks

- **Complexity Analysis**
  - Functions with too many decision paths (if statements, loops, etc.)
  - Deeply nested code blocks
  - Complex conditional statements

- **Code Smells**
  - Nested loops beyond 2 levels
  - Long functions
  - Redundant code patterns

- **Optimization Opportunities**
  - List comprehension suggestions
  - Loop optimizations
  - Data structure improvements

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

See examples in the `examples` folder.

The generated report will include:

- File-by-file analysis
- Line numbers for issues
- Description of problems
- Suggested improvements
- Optimized code snippets when available

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
