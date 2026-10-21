import json
from pathlib import Path


def read_json_file(file_path):
    """Read JSON from a file and provide a useful error for missing files."""
    path = Path(file_path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Input file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {path} at line {error.lineno}, column {error.colno}."
        ) from error


def write_json_file(file_path, data):
    """Write Python data as readable JSON."""
    path = Path(file_path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
