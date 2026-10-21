from collections import Counter


def count_levels(logs):
    """Count INFO, WARNING and ERROR records."""

    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    for log in logs:

        level = log["level"]

        if level in counts:
            counts[level] += 1

    return counts


def find_top_errors(logs, limit=5):
    """Find the most frequent ERROR messages."""

    error_messages = []

    for log in logs:

        if log["level"] == "ERROR":
            error_messages.append(
                log["message"]
            )

    message_counts = Counter(error_messages)

    return message_counts.most_common(limit)


def filter_by_level(logs, level):
    """Return logs matching the requested level."""

    level = level.upper()

    return [
        log
        for log in logs
        if log["level"] == level
    ]


def write_error_lines(logs, filename):
    """Write ERROR records into a separate file."""

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        for log in logs:

            if log["level"] == "ERROR":

                file.write(
                    f"{log['timestamp']} "
                    f"{log['level']} "
                    f"{log['message']}\n"
                )


def print_summary(
    filename,
    logs,
    counts,
    top_errors,
    requested_level=None
):
    """Print the final log analysis report."""

    print()

    print("=" * 60)
    print("                 SERVER LOG REPORT")
    print("=" * 60)

    print(f"File              : {filename}")

    if requested_level:
        print(
            f"Requested level   : "
            f"{requested_level}"
        )

    print(
        f"Valid records     : "
        f"{len(logs)}"
    )

    print()

    print("LOG LEVEL COUNTS")
    print("-" * 60)

    print(
        f"INFO              : "
        f"{counts['INFO']}"
    )

    print(
        f"WARNING           : "
        f"{counts['WARNING']}"
    )

    print(
        f"ERROR             : "
        f"{counts['ERROR']}"
    )

    print()

    print("TOP ERROR MESSAGES")
    print("-" * 60)

    if not top_errors:

        print("No ERROR messages found.")

    else:

        for number, (message, count) in enumerate(
            top_errors,
            start=1
        ):

            print(
                f"{number}. "
                f"{message} - "
                f"{count}"
            )

    print()
    print("=" * 60)