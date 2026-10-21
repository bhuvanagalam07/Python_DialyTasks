
import argparse
import csv
import logging
import sys

from logger_config import setup_logging
from processor import process_csv


def main():
    parser = argparse.ArgumentParser(
        description="Clean and validate employee data in a CSV file."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Output directory (default: output)",
    )

    args = parser.parse_args()

    try:
        setup_logging(args.output)
        summary = process_csv(args.input_file, args.output)

    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        logging.error("Processing failed: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("\nProcessing completed successfully.")
    print(f"Total rows:     {summary['total_rows']}")
    print(f"Valid rows:     {summary['valid_rows']}")
    print(f"Invalid rows:   {summary['invalid_rows']}")
    print(f"Duplicate rows: {summary['duplicate_rows']}")
    print(f"Output folder:  {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
