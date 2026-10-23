"""Application configuration and defaults."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_ROOT / "data" / "sample_weather.json"
DEFAULT_REPORT_DIR = PROJECT_ROOT / "reports"
DEFAULT_TIMEOUT_SECONDS = 5
DEFAULT_MAX_RETRIES = 2
