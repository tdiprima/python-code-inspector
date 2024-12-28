"""
Unit tests for the code analyzer functionality.
"""
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from pyrefactor import analyze_code, generate_tests


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
    issues = analyze_code(source_code)
    nested_loop_issues = [i for i in issues if i.issue_type == "nested_loops"]

    assert len(nested_loop_issues) > 0
    assert "nested loops detected" in nested_loop_issues[0].description.lower()


def test_list_comprehension_detection():
    source_code = """
def get_squares(numbers):
    squares = []
    for num in numbers:
        squares.append(num * num)
    return squares
"""
    issues = analyze_code(source_code)
    comprehension_issues = [i for i in issues if i.issue_type == "list_comprehension"]

    assert len(comprehension_issues) > 0
    assert "list comprehension" in comprehension_issues[0].description.lower()
    assert "[" in comprehension_issues[0].optimized_code
    assert "]" in comprehension_issues[0].optimized_code


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
    issues = analyze_code(source_code)
    complexity_issues = [i for i in issues if i.issue_type == "high_complexity"]

    assert len(complexity_issues) > 0
    assert "complexity" in complexity_issues[0].description.lower()


def test_test_generation():
    source_code = """
def calculate_average(numbers):
    if not numbers:
        return None
    return sum(numbers) / len(numbers)
"""
    tests = generate_tests(source_code, "stats")

    assert "import unittest" in tests
    assert "class TestStats" in tests
    assert "test_calculate_average" in tests
    assert "self.assertIsNotNone" in tests


def test_empty_code():
    issues = analyze_code("")
    assert len(issues) == 0


def test_syntax_error():
    source_code = "def invalid_syntax:"
    with pytest.raises(SyntaxError):
        analyze_code(source_code)
