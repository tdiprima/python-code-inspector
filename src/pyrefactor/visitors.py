import ast
from .models import CodeIssue


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


class TestCaseVisitor(ast.NodeVisitor):
    """Collect information about functions for test generation."""

    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append(node)
        self.generic_visit(node)
