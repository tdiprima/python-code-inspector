"""
pyrefactor-ai - AI-powered Python code refactoring and optimization assistant.
Exposes the main public API functions.
"""

from .analyzer import analyze_code, generate_tests
from .models import CodeIssue

__version__ = "0.1.0"
__all__ = ["analyze_code", "generate_tests", "CodeIssue"]
