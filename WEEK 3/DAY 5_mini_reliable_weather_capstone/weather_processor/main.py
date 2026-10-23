"""CLI entry point for the weather data-processing capstone."""
import argparse
import json
import logging
import sys
from pathlib import Path
from .api_client import ApiClientError, WeatherApiClient
from .config import DEFAULT_INPUT, DEFAULT_REPORT_DIR, DEFAULT_TIMEOUT_SECONDS, DEFAULT_MAX_RETRIES
from .processor import process_weather_data
from .report_generator import ReportError, write_reports
from .validator import DataValidationError


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DataValidationError(f"Input file contains invalid JSON: {path}") from exc
    except OSError as exc:
        raise OSError(f"Could not read input file: {path}") from exc


def build_parser():
    parser = argparse.ArgumentParser(description="Process weather records and generate JSON/CSV reports.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="JSON file containing sample weather records (default: bundled sample data)")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_REPORT_DIR, help="Directory for generated reports")
    parser.add_argument("--live", action="store_true", help="Fetch one live observation using Open-Meteo instead of reading the sample file")
    parser.add_argument("--city", default="Hyderabad", help="City label used with --live")
    parser.add_argument("--latitude", type=float, default=17.385, help="Latitude used with --live")
    parser.add_argument("--longitude", type=float, default=78.4867, help="Longitude used with --live")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS, help="HTTP timeout in seconds")
    parser.add_argument("--retries", type=int, default=DEFAULT_MAX_RETRIES, help="Maximum retries for transient API errors")
    return parser


def run(args) -> int:
    try:
        if args.live:
            client = WeatherApiClient(timeout=args.timeout, max_retries=args.retries)
            records = [client.get_current_weather(args.city, args.latitude, args.longitude)]
            source = "live_api"
        else:
            records = load_json(args.input)
            source = "sample_file"
        summary = process_weather_data(records)
        summary["data_source"] = source
        json_path, csv_path = write_reports(summary, args.output_dir)
        print("Weather data processing completed successfully.")
        print(f"Data source: {source}")
        print(f"Cities processed: {summary['total_cities']}")
        print(f"Average temperature: {summary['average_temperature']:.2f} C")
        print(f"Hottest city: {summary['hottest_city']} ({summary['highest_temperature']:.2f} C)")
        print(f"Coldest city: {summary['coldest_city']} ({summary['lowest_temperature']:.2f} C)")
        print(f"JSON report: {json_path}")
        print(f"CSV report: {csv_path}")
        return 0
    except (ApiClientError, DataValidationError, FileNotFoundError, OSError, ReportError, ValueError) as exc:
        logging.error("Application failed safely: %s", exc)
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return run(build_parser().parse_args(argv))

if __name__ == "__main__":
    raise SystemExit(main())
