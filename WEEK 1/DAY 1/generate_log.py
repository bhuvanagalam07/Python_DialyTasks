from datetime import datetime, timedelta
import random


messages = {
    "INFO": [
        "Request completed successfully",
        "User authenticated",
        "Database connection established",
        "Health check passed",
        "Cache refreshed",
    ],
    "WARNING": [
        "High memory usage detected",
        "Slow database response",
        "Connection pool nearly full",
        "Retrying external request",
    ],
    "ERROR": [
        "Database connection failed",
        "Authentication failed",
        "Timeout while contacting service",
        "File not found",
        "Internal server error",
    ],
}


start_time = datetime(2026, 10, 5, 9, 0, 0)

with open("sample_server.log", "w", encoding="utf-8") as log_file:
    for number in range(600):
        timestamp = start_time + timedelta(seconds=number)
        level = random.choices(
            ["INFO", "WARNING", "ERROR"],
            weights=[70, 20, 10],
        )[0]

        message = random.choice(messages[level])

        log_file.write(
            f"{timestamp.isoformat()} {level} {message}\n"
        )

print("Generated 600 log lines.")
