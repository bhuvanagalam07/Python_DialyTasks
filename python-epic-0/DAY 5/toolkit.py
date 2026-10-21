import argparse
import sys

from api_monitor import ApiMonitor
from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator


def run_logs(args):
    """Run the log analyzer command."""
    analyzer = LogAnalyzer(args.file)
    analyzer.display_report()


def run_report(args):
    """Run the employee report command."""
    generator = ReportGenerator(args.input)
    report = generator.generate_report(args.output)

    print("\n===== EMPLOYEE REPORT =====")
    print(f"Total employees: {report['total_employees']}")

    print("\nDepartment statistics:")
    for department, stats in report["department_statistics"].items():
        print(
            f"{department}: "
            f"{stats['employee_count']} employees, "
            f"average salary {stats['average_salary']:.2f}"
        )

    print(
        "\nEmployees who joined in the last 90 days: "
        f"{len(report['employees_joined_last_90_days'])}"
    )
    print(f"Report saved to: {args.output}")


def run_monitor(args):
    """Run the API monitor command."""
    monitor = ApiMonitor()
    urls = monitor.load_urls(args.urls)
    results = monitor.monitor(urls)
    monitor.save_results(results, args.output)
    print(f"\nMonitoring results saved to: {args.output}")


def build_parser():
    """Configure command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Ops Toolkit: logs, employee reports, and API monitoring.",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Logs command
    logs_parser = subparsers.add_parser(
        "logs",
        help="Analyze application logs",
    )
    logs_parser.add_argument(
        "--file",
        default="app.log",
        help="Path to the log file (default: app.log)",
    )
    logs_parser.set_defaults(func=run_logs)

    # Report command
    report_parser = subparsers.add_parser(
        "report",
        help="Generate an employee report",
    )
    report_parser.add_argument(
        "--input",
        default="employees.csv",
        help="Input employee CSV file",
    )
    report_parser.add_argument(
        "--output",
        default="reports/employee_report.json",
        help="Output report JSON file",
    )
    report_parser.set_defaults(func=run_report)

    # Monitor command
    monitor_parser = subparsers.add_parser(
        "monitor",
        help="Monitor API URLs",
    )
    monitor_parser.add_argument(
        "--urls",
        default="urls.txt",
        help="Text file containing API URLs",
    )
    monitor_parser.add_argument(
        "--output",
        default="reports/api_data.json",
        help="Output JSON file for monitoring results",
    )
    monitor_parser.set_defaults(func=run_monitor)

    return parser


def main(argv=None):
    """Run the selected toolkit command."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return

    try:
        args.func(args)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        raise SystemExit(130)


if __name__ == "__main__":
    main()
