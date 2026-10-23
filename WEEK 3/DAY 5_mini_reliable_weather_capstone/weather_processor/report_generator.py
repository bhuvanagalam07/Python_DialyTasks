"""Safe JSON and CSV report output."""
import csv
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

class ReportError(RuntimeError):
    """Raised when a report cannot be written."""


def write_reports(summary: dict[str, Any], output_dir: str | Path) -> tuple[Path, Path]:
    directory = Path(output_dir)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        payload = {**summary, "generated_at_utc": datetime.now(timezone.utc).isoformat()}
        json_path = directory / "weather_report.json"
        csv_path = directory / "weather_report.csv"
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["city", "temperature"])
            writer.writeheader()
            writer.writerows(summary["records"])
        logger.info("Reports written: %s and %s", json_path, csv_path)
        return json_path, csv_path
    except (OSError, KeyError, TypeError, ValueError) as exc:
        logger.error("Report generation failed: %s", exc)
        raise ReportError(f"Could not write reports to '{directory}'. Check the path and permissions.") from exc
