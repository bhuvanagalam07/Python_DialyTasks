from dataclasses import dataclass
from datetime import datetime


class BaseAnalyzer:
    """Base class for toolkit analyzers."""

    def __init__(self, name):
        self.name = name

    def display_name(self):
        return f"Analyzer: {self.name}"


class LogAnalyzerModel(BaseAnalyzer):
    """Demonstrate inheritance."""

    def __init__(self, name, log_file):
        super().__init__(name)
        self.log_file = log_file


@dataclass
class ApiResult:
    """Store the result of an API check."""

    url: str
    status_code: int | None
    response_time: float
    success: bool
    checked_at: datetime
