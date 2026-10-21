from collections import Counter
from pathlib import Path


class LogAnalyzer:
    """Analyze application log files."""

    def __init__(self, log_file):
        self.log_file = Path(log_file)

    def read_logs(self):
        """Read log lines from the file."""
        if not self.log_file.exists():
            raise FileNotFoundError(f"Log file not found: {self.log_file}")

        with self.log_file.open("r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]

    def analyze(self):
        """Count log levels and collect error messages."""
        lines = self.read_logs()
        counts = Counter()
        errors = []
        warnings = []

        for line in lines:
            parts = line.split()

            if len(parts) < 3:
                counts["UNKNOWN"] += 1
                continue

            level = parts[2].upper()
            counts[level] += 1

            if level == "ERROR":
                errors.append(line)
            elif level in ("WARNING", "WARN"):
                warnings.append(line)

        return {
            "total_lines": len(lines),
            "counts": dict(counts),
            "errors": errors,
            "warnings": warnings,
        }

    def display_report(self):
        """Display a summary of the log file."""
        report = self.analyze()

        print("\n===== LOG ANALYSIS REPORT =====")
        print(f"Total log lines: {report['total_lines']}")

        for level, count in sorted(report["counts"].items()):
            print(f"{level}: {count}")

        print("\nError messages:")
        if report["errors"]:
            for error in report["errors"]:
                print(error)
        else:
            print("No errors found.")

        print("\nWarning messages:")
        if report["warnings"]:
            for warning in report["warnings"]:
                print(warning)
        else:
            print("No warnings found.")
