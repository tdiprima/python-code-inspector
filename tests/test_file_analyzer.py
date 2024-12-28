"""
Unit tests for the code analyzer functionality.
"""

import os
import tempfile
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from pyrefactor.file_analyzer import ProjectAnalyzer, FileAnalysis


def create_temp_file(content: str) -> Path:
    """Helper function to create a temporary Python file with given content."""
    fd, path = tempfile.mkstemp(suffix='.py')
    os.close(fd)
    with open(path, 'w') as f:
        f.write(content)
    return Path(path)


def test_nested_loops_detection():
    source_code = """
def process_matrix(matrix):
    result = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            for k in range(len(matrix[i][j])):
                result.append(matrix[i][j][k])
    return result
"""
    temp_file = create_temp_file(source_code)
    try:
        analyzer = ProjectAnalyzer(str(temp_file.parent))
        results = analyzer.analyze_project()

        # Get analysis for our temp file
        analysis = results[str(temp_file)]
        nested_loop_issues = [i for i in analysis.issues if i.issue_type == "nested_loops"]

        assert len(nested_loop_issues) > 0
        assert "nested loops detected" in nested_loop_issues[0].description.lower()
    finally:
        temp_file.unlink()  # Clean up temp file


def test_list_comprehension_detection():
    source_code = """
def get_squares(numbers):
    squares = []
    for num in numbers:
        squares.append(num * num)
    return squares
"""
    temp_file = create_temp_file(source_code)
    try:
        analyzer = ProjectAnalyzer(str(temp_file.parent))
        results = analyzer.analyze_project()

        analysis = results[str(temp_file)]
        comprehension_issues = [i for i in analysis.issues if i.issue_type == "list_comprehension"]

        assert len(comprehension_issues) > 0
        assert "list comprehension" in comprehension_issues[0].description.lower()
        assert "[" in comprehension_issues[0].optimized_code
        assert "]" in comprehension_issues[0].optimized_code
    finally:
        temp_file.unlink()


def test_complexity_detection():
    source_code = """
def complex_function(x):
    if x < 0:
        if x < -10:
            return "very negative"
        elif x < -5:
            return "moderately negative"
        else:
            return "slightly negative"
    else:
        if x > 10:
            return "very positive"
        elif x > 5:
            return "moderately positive"
        else:
            return "slightly positive"
"""
    temp_file = create_temp_file(source_code)
    try:
        analyzer = ProjectAnalyzer(str(temp_file.parent))
        results = analyzer.analyze_project()

        analysis = results[str(temp_file)]
        complexity_issues = [i for i in analysis.issues if i.issue_type == "high_complexity"]

        assert len(complexity_issues) > 0
        assert "complexity" in complexity_issues[0].description.lower()
    finally:
        temp_file.unlink()


def test_empty_file():
    temp_file = create_temp_file("")
    try:
        analyzer = ProjectAnalyzer(str(temp_file.parent))
        results = analyzer.analyze_project()

        analysis = results[str(temp_file)]
        assert len(analysis.issues) == 0
        assert analysis.error is None
    finally:
        temp_file.unlink()


def test_syntax_error():
    temp_file = create_temp_file("def invalid_syntax:")
    try:
        analyzer = ProjectAnalyzer(str(temp_file.parent))
        results = analyzer.analyze_project()

        analysis = results[str(temp_file)]
        assert analysis.error is not None
        assert "SyntaxError" in analysis.error
    finally:
        temp_file.unlink()


def test_excluded_files():
    temp_file = create_temp_file("def some_function(): pass")
    try:
        analyzer = ProjectAnalyzer(str(temp_file.parent), exclude_files=[temp_file.name])
        results = analyzer.analyze_project()

        assert str(temp_file) not in results
    finally:
        temp_file.unlink()


def test_report_generation():
    source_code = """
def simple_function():
    pass
"""
    temp_file = create_temp_file(source_code)
    try:
        analyzer = ProjectAnalyzer(str(temp_file.parent))
        results = analyzer.analyze_project()

        # Generate report to string (no file output)
        report = analyzer.generate_report(results)

        assert "Code Analysis Report" in report
        assert str(temp_file) in report
    finally:
        temp_file.unlink()
