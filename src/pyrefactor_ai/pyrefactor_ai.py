import ast
import astroid
import pylint.lint
import radon.complexity
import typing
from dataclasses import dataclass
from pathlib import Path
import inspect

@dataclass
class CodeIssue:
    """Represents a detected code issue with suggested improvements."""
    line_number: int
    issue_type: str
    description: str
    suggestion: str
    original_code: str
    optimized_code: str = None

class CodeAnalyzer:
    """Main class for analyzing and refactoring Python code."""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.ast_tree = ast.parse(source_code)
        self.issues: list[CodeIssue] = []

    def analyze(self) -> list[CodeIssue]:
        """Perform comprehensive code analysis."""
        self._analyze_complexity()
        self._detect_code_smells()
        self._find_optimization_opportunities()
        return self.issues

    def _analyze_complexity(self):
        """Analyze cyclomatic complexity of the code."""
        visitor = ComplexityVisitor()
        visitor.visit(self.ast_tree)
        
        for func_node, complexity in visitor.complexities.items():
            if complexity > 10:  # McCabe complexity threshold
                self.issues.append(CodeIssue(
                    line_number=func_node.lineno,
                    issue_type="high_complexity",
                    description=f"Function '{func_node.name}' has high cyclomatic complexity ({complexity})",
                    suggestion="Consider breaking down this function into smaller, more focused functions",
                    original_code=self._get_node_source(func_node)
                ))

    def _detect_code_smells(self):
        """Detect common code smells."""
        visitor = CodeSmellVisitor()
        visitor.visit(self.ast_tree)
        
        for issue in visitor.issues:
            self.issues.append(issue)

    def _find_optimization_opportunities(self):
        """Identify potential optimization opportunities."""
        visitor = OptimizationVisitor()
        visitor.visit(self.ast_tree)
        
        for issue in visitor.issues:
            self.issues.append(issue)

    def _get_node_source(self, node: ast.AST) -> str:
        """Extract source code for a given AST node."""
        lines = self.source_code.splitlines()
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            return '\n'.join(lines[node.lineno-1:node.end_lineno])
        return ""

    def generate_unit_tests(self, module_name: str) -> str:
        """Generate unit tests for the analyzed code."""
        test_generator = UnitTestGenerator(self.ast_tree, module_name)
        return test_generator.generate_tests()

class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor to calculate cyclomatic complexity."""
    
    def __init__(self):
        self.complexities = {}
        self.current_complexity = 0

    def visit_FunctionDef(self, node):
        previous_complexity = self.current_complexity
        self.current_complexity = 1  # Base complexity
        
        # Visit all children
        self.generic_visit(node)
        
        self.complexities[node] = self.current_complexity
        self.current_complexity = previous_complexity

    def visit_If(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

class CodeSmellVisitor(ast.NodeVisitor):
    """AST visitor to detect code smells."""
    
    def __init__(self):
        self.issues = []
        self.loop_depth = 0

    def visit_For(self, node):
        self.loop_depth += 1
        if self.loop_depth > 2:
            self.issues.append(CodeIssue(
                line_number=node.lineno,
                issue_type="nested_loops",
                description="Deeply nested loops detected",
                suggestion="Consider restructuring the code to reduce nesting depth",
                original_code=ast.unparse(node)
            ))
        self.generic_visit(node)
        self.loop_depth -= 1

class OptimizationVisitor(ast.NodeVisitor):
    """AST visitor to identify optimization opportunities."""
    
    def __init__(self):
        self.issues = []

    def visit_For(self, node):
        # Check for list comprehension opportunities
        if isinstance(node.body, list) and len(node.body) == 1:
            if (isinstance(node.body[0], ast.Expr) and 
                isinstance(node.body[0].value, ast.Call) and
                isinstance(node.body[0].value.func, ast.Attribute) and
                node.body[0].value.func.attr == 'append'):
                self.issues.append(CodeIssue(
                    line_number=node.lineno,
                    issue_type="list_comprehension",
                    description="Loop could be replaced with list comprehension",
                    suggestion="Use a list comprehension for better readability and performance",
                    original_code=ast.unparse(node),
                    optimized_code=self._generate_list_comprehension(node)
                ))
        self.generic_visit(node)

    def _generate_list_comprehension(self, node: ast.For) -> str:
        """Generate a list comprehension from a for loop."""
        target = ast.unparse(node.target)
        iter_expr = ast.unparse(node.iter)
        body_expr = ast.unparse(node.body[0].value)
        return f"[{body_expr} for {target} in {iter_expr}]"

class UnitTestGenerator:
    """Generate unit tests for Python code."""
    
    def __init__(self, ast_tree: ast.AST, module_name: str):
        self.ast_tree = ast_tree
        self.module_name = module_name
        self.test_cases = []

    def generate_tests(self) -> str:
        """Generate unit test code."""
        visitor = TestCaseVisitor()
        visitor.visit(self.ast_tree)
        
        test_code = [
            "import unittest",
            f"import {self.module_name}",
            "",
            f"class Test{self.module_name.capitalize()}(unittest.TestCase):",
        ]
        
        for func_node in visitor.functions:
            test_code.extend(self._generate_test_for_function(func_node))
        
        return "\n".join(test_code)

    def _generate_test_for_function(self, func_node: ast.FunctionDef) -> list[str]:
        """Generate test cases for a single function."""
        params = [p.arg for p in func_node.args.args]
        test_name = f"test_{func_node.name}"
        
        return [
            f"    def {test_name}(self):",
            "        # TODO: Add appropriate test cases",
            f"        result = {self.module_name}.{func_node.name}({', '.join(['None'] * len(params))})",
            "        self.assertIsNotNone(result)"
        ]

class TestCaseVisitor(ast.NodeVisitor):
    """Collect information about functions for test generation."""
    
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append(node)
        self.generic_visit(node)

def analyze_code(source_code: str) -> list[CodeIssue]:
    """Main entry point for code analysis."""
    analyzer = CodeAnalyzer(source_code)
    return analyzer.analyze()

def generate_tests(source_code: str, module_name: str) -> str:
    """Generate unit tests for the given source code."""
    analyzer = CodeAnalyzer(source_code)
    return analyzer.generate_unit_tests(module_name)
