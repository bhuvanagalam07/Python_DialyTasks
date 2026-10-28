"""Small JSON repository used by the services."""
import json
from pathlib import Path
from typing import Any


class JSONStorage:
    """Read/write a JSON list of dictionaries, creating files when needed."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write_all([])

    def read_all(self) -> list[dict[str, Any]]:
        """Load all records; an invalid JSON file raises a useful error."""
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {self.path}") from exc
        if not isinstance(data, list) or not all(isinstance(x, dict) for x in data):
            raise ValueError(f"{self.path} must contain a JSON list of objects")
        return data

    def write_all(self, records: list[dict[str, Any]]) -> None:
        """Persist records with readable indentation."""
        self.path.write_text(
            json.dumps(records, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
