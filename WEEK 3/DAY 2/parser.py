import json


def parse_json(raw_text):
    """Convert JSON text to Python data and report malformed JSON clearly."""
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON at line {error.lineno}, column {error.colno}."
        ) from error
