from dataclasses import dataclass


@dataclass
class CodeIssue:
    """Represents a detected code issue with suggested improvements."""
    line_number: int
    issue_type: str
    description: str
    suggestion: str
    original_code: str
    optimized_code: str = None
