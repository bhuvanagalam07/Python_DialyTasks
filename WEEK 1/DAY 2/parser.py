import logging

from exceptions import InvalidLogFormatError


LOG_LEVELS = ("INFO", "WARNING", "ERROR")


def parse_log_line(line):
    """
    Parse one log line.

    Expected format:
    2026-10-06 10:15:20 ERROR Database connection failed

    Returns:
        tuple: timestamp, level, message

    Raises:
        InvalidLogFormatError: If the line is invalid.
    """

    line = line.strip()

    if not line:
        raise InvalidLogFormatError("Log line is empty.")

    parts = line.split(" ", 3)

    if len(parts) != 4:
        raise InvalidLogFormatError(
            f"Invalid log format: {line}"
        )

    date = parts[0]
    time = parts[1]
    level = parts[2].upper()
    message = parts[3]

    if level not in LOG_LEVELS:
        raise InvalidLogFormatError(
            f"Invalid log level: {level}"
        )

    if not message.strip():
        raise InvalidLogFormatError(
            "Log message is empty."
        )

    timestamp = f"{date} {time}"

    return timestamp, level, message


def read_log_file(filename):
    """
    Read the log file and return valid log records.
    """

    logs = []

    try:
        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            for line_number, line in enumerate(
                file,
                start=1
            ):

                try:
                    parsed = parse_log_line(line)

                    timestamp, level, message = parsed

                    logs.append({
                        "timestamp": timestamp,
                        "level": level,
                        "message": message
                    })

                except InvalidLogFormatError as error:

                    logging.warning(
                        "Skipping malformed line %s: %s",
                        line_number,
                        error
                    )

    except FileNotFoundError:

        raise FileNotFoundError(
            f"Log file '{filename}' was not found."
        )

    except PermissionError:

        raise PermissionError(
            f"Permission denied while reading '{filename}'."
        )

    except OSError as error:

        raise OSError(
            f"Unable to read '{filename}': {error}"
        )

    finally:

        logging.debug(
            "Finished reading file: %s",
            filename
        )

    return logs