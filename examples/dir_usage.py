"""
Directory Scan: Better for when you want to analyze an entire project at once
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from pyrefactor.file_analyzer import ProjectAnalyzer

# Analyze a single directory
analyzer = ProjectAnalyzer(
    root_path="./my_project",
    exclude_dirs=['tests', 'venv'],
    exclude_files=['setup.py']
)

# Run the analysis
results = analyzer.analyze_project()

# Generate and save a report
analyzer.generate_report(results, output_file="analysis_report.md")
