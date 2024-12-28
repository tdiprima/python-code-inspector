import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional

from .analyzer import analyze_code
from .models import CodeIssue


@dataclass
class FileAnalysis:
    """Results of analyzing a single Python file."""
    filepath: Path
    issues: List[CodeIssue]
    error: Optional[str] = None


class ProjectAnalyzer:
    """Analyzes Python files in a directory structure."""

    def __init__(self, root_path: str, exclude_dirs: List[str] = None, exclude_files: List[str] = None):
        self.root_path = Path(root_path)
        self.exclude_dirs = set(exclude_dirs or ['venv', '.git', '__pycache__', 'build', 'dist'])
        self.exclude_files = set(exclude_files or [])

    def analyze_project(self) -> Dict[str, FileAnalysis]:
        """
        Analyze all Python files in the project directory.
        
        Returns:
            Dict mapping file paths to their analysis results
        """
        results = {}

        for filepath in self._find_python_files():
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    source_code = file.read()

                issues = analyze_code(source_code)
                results[str(filepath)] = FileAnalysis(filepath=filepath, issues=issues)

            except Exception as e:
                results[str(filepath)] = FileAnalysis(filepath=filepath, issues=[], error=f"{type(e).__name__}: {str(e)}")

        return results

    def _find_python_files(self) -> List[Path]:
        """Recursively find all Python files in the project."""
        python_files = []

        for root, dirs, files in os.walk(self.root_path):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]

            for file in files:
                if file.endswith('.py') and file not in self.exclude_files:
                    python_files.append(Path(root) / file)

        return python_files

    def generate_report(self, results: Dict[str, FileAnalysis], output_file: str = None):
        """Generate a markdown report from analysis results."""
        report = ["# Code Analysis Report\n"]

        total_issues = sum(len(analysis.issues) for analysis in results.values())
        report.append(f"Total files analyzed: {len(results)}")
        report.append(f"Total issues found: {total_issues}\n")

        for filepath, analysis in sorted(results.items()):
            report.append(f"## {filepath}")

            if analysis.error:
                report.append(f"\n⚠️ Error: {analysis.error}\n")
                continue

            if not analysis.issues:
                report.append("\n✅ No issues found\n")
                continue

            for issue in analysis.issues:
                report.append(f"\n### Line {issue.line_number}: {issue.issue_type}")
                report.append(f"**Description:** {issue.description}")
                report.append(f"**Suggestion:** {issue.suggestion}")
                report.append("\n**Original Code:**")
                report.append(f"```python\n{issue.original_code}\n```")

                if issue.optimized_code:
                    report.append("\n**Optimized Code:**")
                    report.append(f"```python\n{issue.optimized_code}\n```")

        report_content = '\n'.join(report)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)

        return report_content
