"""
Unit tests for the AST visitors.
"""

import ast
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from pyrefactor.visitors import (
    ComplexityVisitor,
    CodeSmellVisitor,
    OptimizationVisitor,
    CaseVisitor
)


def test_complexity_visitor():
    source = """
def simple_function():
    return 1

def complex_function(x):
    if x > 0:
        if x > 10:
            return "high"
        return "positive"
    else:
        return "negative"
"""
    tree = ast.parse(source)
    visitor = ComplexityVisitor()
    visitor.visit(tree)

    complexities = {node.name: complexity
                   for node, complexity in visitor.complexities.items()}

    assert complexities["simple_function"] == 1
    assert complexities["complex_function"] > complexities["simple_function"]


def test_code_smell_visitor():
    source = """
def nested_loops():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                print(i, j, k)
"""
    tree = ast.parse(source)
    visitor = CodeSmellVisitor()
    visitor.visit(tree)

    assert len(visitor.issues) > 0
    assert visitor.issues[0].issue_type == "nested_loops"


def test_optimization_visitor():
    source = """
def build_squares():
    squares = []
    for i in range(10):
        squares.append(i * i)
    return squares
"""
    tree = ast.parse(source)
    visitor = OptimizationVisitor()
    visitor.visit(tree)

    assert len(visitor.issues) > 0
    assert visitor.issues[0].issue_type == "list_comprehension"
    assert "i * i" in visitor.issues[0].optimized_code


def test_test_case_visitor():
    source = """
def func1():
    pass

def func2(x, y):
    return x + y
"""
    tree = ast.parse(source)
    visitor = CaseVisitor()
    visitor.visit(tree)

    function_names = [node.name for node in visitor.functions]
    assert "func1" in function_names
    assert "func2" in function_names
    assert len(function_names) == 2
