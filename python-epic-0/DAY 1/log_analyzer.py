from collections import Counter


VALID_LEVELS = {"INFO", "WARNING", "ERROR"}


def parse_log_line(line):
    """Parse one log line into timestamp, level, and message."""

    parts = line.strip().split(" ", 2)

    if len(parts) != 3:
        return None

    timestamp, level, message = parts

    if level not in VALID_LEVELS or not message:
        return None

    return timestamp, level, message


def analyze_log(input_file, error_file):
    """Read a server log and produce a summary."""

    level_counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
    }

    error_messages = Counter()
    total_lines = 0
    malformed_lines = 0

    try:
        with open(input_file, "r", encoding="utf-8") as log_file:
            with open(error_file, "w", encoding="utf-8") as errors_file:

                for line in log_file:
                    total_lines += 1

                    parsed = parse_log_line(line)

                    if parsed is None:
                        malformed_lines += 1
                        continue

                    timestamp, level, message = parsed
                    level_counts[level] += 1

                    if level == "ERROR":
                        error_messages[message] += 1
                        errors_file.write(line)

    except FileNotFoundError:
        print(f"Error: input file '{input_file}' was not found.")
        return

    print("\n===== SERVER LOG SUMMARY =====")
    print(f"Total lines:      {total_lines}")
    print(f"INFO:             {level_counts['INFO']}")
    print(f"WARNING:          {level_counts['WARNING']}")
    print(f"ERROR:            {level_counts['ERROR']}")
    print(f"Malformed lines:  {malformed_lines}")

    print("\nTop 5 error messages:")

    if not error_messages:
        print("No error messages found.")
    else:
        for message, count in error_messages.most_common(5):
            print(f"{count:>3}x - {message}")

    print(f"\nERROR lines written to: {error_file}")


def main():
    """Program entry point."""

    input_file = "sample_server.log"
    error_file = "errors_only.log"

    analyze_log(input_file, error_file)


if __name__ == "__main__":
    main()
