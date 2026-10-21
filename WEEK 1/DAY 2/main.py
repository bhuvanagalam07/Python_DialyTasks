import argparse
import logging
import os

from parser import read_log_file

from report import (
    count_levels,
    find_top_errors,
    filter_by_level,
    write_error_lines,
    print_summary
)


# Folder where this script lives. All default paths are built from it,
# so the program works no matter which directory the terminal is in.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def setup_logging():
    """Configure application logging."""

    logging.basicConfig(
        filename=os.path.join(BASE_DIR, "app.log"),
        level=logging.INFO,
        format=(
            "%(asctime)s - "
            "%(levelname)s - "
            "%(message)s"
        )
    )


def create_parser():
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Analyze a server log file "
            "and generate a report."
        )
    )

    parser.add_argument(
        "--file",
        default=os.path.join(BASE_DIR, "sample_server.log"),
        help=(
            "Path to the log file "
            "(default: sample_server.log next to main.py)."
        )
    )

    parser.add_argument(
        "--level",
        choices=[
            "INFO",
            "WARNING",
            "ERROR"
        ],
        default="ERROR",
        help="Log level to filter."
    )

    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of top error messages."
    )

    return parser


def main():
    """Run the log analyzer application."""

    setup_logging()

    parser = create_parser()

    args = parser.parse_args()

    logging.info(
        "Starting log analysis for %s",
        args.file
    )

    try:

        logs = read_log_file(
            args.file
        )

        counts = count_levels(
            logs
        )

        top_errors = find_top_errors(
            logs,
            args.top
        )

        filtered_logs = filter_by_level(
            logs,
            args.level
        )

        output_file = os.path.join(BASE_DIR, "errors_only.log")

        write_error_lines(
            logs,
            output_file
        )

        print_summary(
            args.file,
            logs,
            counts,
            top_errors,
            args.level
        )

        print(
            f"\n{args.level} records found: "
            f"{len(filtered_logs)}"
        )

        logging.info(
            "Log analysis completed successfully."
        )

    except FileNotFoundError as error:

        logging.error(str(error))

        print(
            f"Error: {error}"
        )

    except PermissionError as error:

        logging.error(str(error))

        print(
            f"Error: {error}"
        )

    except OSError as error:

        logging.error(str(error))

        print(
            f"Error: {error}"
        )

    except ValueError as error:

        logging.error(str(error))

        print(
            f"Error: {error}"
        )

    finally:

        logging.info(
            "Log analyzer execution finished."
        )


if __name__ == "__main__":
    main()