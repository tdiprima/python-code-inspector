import ast
from typing import List

from .generators import UnitTestGenerator
from .models import CodeIssue
from .visitors import ComplexityVisitor, CodeSmellVisitor, OptimizationVisitor


class CodeAnalyzer:
    """Main class for analyzing and refactoring Python code."""

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.ast_tree = ast.parse(source_code)
        self.issues: List[CodeIssue] = []

    def analyze(self) -> List[CodeIssue]:
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
            return '\n'.join(lines[node.lineno - 1:node.end_lineno])
        return ""

    def generate_unit_tests(self, module_name: str) -> str:
        """Generate unit tests for the analyzed code."""
        test_generator = UnitTestGenerator(self.ast_tree, module_name)
        return test_generator.generate_tests()


def analyze_code(source_code: str) -> List[CodeIssue]:
    """Main entry point for code analysis."""
    analyzer = CodeAnalyzer(source_code)
    return analyzer.analyze()


def generate_tests(source_code: str, module_name: str) -> str:
    """Generate unit tests for the given source code."""
    analyzer = CodeAnalyzer(source_code)
    return analyzer.generate_unit_tests(module_name)
