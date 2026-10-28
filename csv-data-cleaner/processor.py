
import csv
import json
import logging
from pathlib import Path

from validator import REQUIRED_COLUMNS, validate_headers, validate_row

logger = logging.getLogger(__name__)


def process_csv(input_file, output_dir):
    """Process a CSV file and return a summary dictionary."""
    input_path = Path(input_file)
    output_path = Path(output_dir)

    # Create the output folder if it does not exist.
    output_path.mkdir(parents=True, exist_ok=True)

    cleaned_file = output_path / "cleaned.csv"
    invalid_file = output_path / "invalid_rows.csv"
    summary_file = output_path / "summary.json"

    total_rows = 0
    valid_rows = 0
    invalid_rows = 0
    duplicate_rows = 0
    seen = set()

    logger.info("Starting CSV processing: %s", input_path)

    # utf-8-sig also handles files with a UTF-8 byte-order mark.
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, strict=True)

        validate_headers(reader.fieldnames)

        with (
            cleaned_file.open("w", encoding="utf-8", newline="") as clean_out,
            invalid_file.open("w", encoding="utf-8", newline="") as invalid_out,
        ):
            clean_writer = csv.DictWriter(
                clean_out, fieldnames=REQUIRED_COLUMNS
            )
            invalid_writer = csv.DictWriter(
                invalid_out,
                fieldnames=REQUIRED_COLUMNS + ["error_reason"],
            )

            clean_writer.writeheader()
            invalid_writer.writeheader()

            for row in reader:
                total_rows += 1

                errors = validate_row(row)

                if errors:
                    invalid_rows += 1
                    invalid_record = {
                        column: (row.get(column) or "").strip()
                        for column in REQUIRED_COLUMNS
                    }
                    invalid_record["error_reason"] = "; ".join(errors)
                    invalid_writer.writerow(invalid_record)
                    logger.warning(
                        "Rejected CSV row %d: %s",
                        total_rows,
                        "; ".join(errors),
                    )
                    continue

                # Normalize whitespace and email capitalization.
                record = {
                    column: (row.get(column) or "").strip()
                    for column in REQUIRED_COLUMNS
                }
                record["email"] = record["email"].lower()

                # A duplicate is a repeated normalized name/email/age tuple.
                key = (
                    record["name"].casefold(),
                    record["email"],
                    int(record["age"]),
                )

                if key in seen:
                    duplicate_rows += 1
                    logger.info(
                        "Skipped duplicate CSV row %d", total_rows
                    )
                    continue

                seen.add(key)
                clean_writer.writerow(record)
                valid_rows += 1

    summary = {
        "input_file": str(input_path),
        "total_rows": total_rows,
        "valid_rows": valid_rows,
        "invalid_rows": invalid_rows,
        "duplicate_rows": duplicate_rows,
    }

    with summary_file.open("w", encoding="utf-8") as summary_out:
        json.dump(summary, summary_out, indent=2)

    logger.info(
        "Processing complete: total=%d valid=%d invalid=%d duplicates=%d",
        total_rows, valid_rows, invalid_rows, duplicate_rows,
    )

    return summary
