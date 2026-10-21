"""Command-line entry point for the Employee Data Processor."""
import argparse
import logging
from pathlib import Path

from employee_app.processor import EmployeeProcessor
from employee_app.reporting import write_reports

def configure_logging(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        encoding="utf-8",
        force=True,
    )

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate employee CSV data and generate reports.")
    parser.add_argument("--input", default="data/employees.csv", help="Input employee CSV path")
    parser.add_argument("--output-dir", default="reports", help="Directory for generated reports")
    parser.add_argument("--log", default="logs/app.log", help="Log file path")
    return parser

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(Path(args.log))
    logger = logging.getLogger(__name__)
    try:
        processor = EmployeeProcessor()
        result = processor.process_csv(Path(args.input))
        paths = write_reports(result, Path(args.output_dir))
        logger.info(
            "Processing complete: %s valid, %s rejected",
            len(result.valid_employees), len(result.rejected_rows)
        )
        print(f"Valid employees: {len(result.valid_employees)}")
        print(f"Rejected rows: {len(result.rejected_rows)}")
        print("Reports generated:")
        for path in paths:
            print(f"  - {path}")
        print(f"Log file: {args.log}")
        return 0
    except (FileNotFoundError, ValueError, OSError) as exc:
        logger.error("Processing failed: %s", exc)
        print(f"Error: {exc}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
