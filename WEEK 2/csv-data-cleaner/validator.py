
import re

REQUIRED_COLUMNS = ["name", "email", "age"]

# A practical email-format check, not a guarantee that an address exists.
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_headers(headers):
    """Check that all required columns exist exactly once."""
    if not headers:
        raise ValueError("The CSV file is empty or has no header row.")

    if len(headers) != len(set(headers)):
        raise ValueError("The CSV contains duplicate column names.")

    missing = [column for column in REQUIRED_COLUMNS
               if column not in headers]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )


def validate_row(row):
    """Return a list of validation errors for one record."""
    errors = []

    # Reject rows containing more values than the header defines.
    if None in row:
        errors.append("Row contains extra values")

    name = (row.get("name") or "").strip()
    email = (row.get("email") or "").strip()
    age_text = (row.get("age") or "").strip()

    if not name:
        errors.append("Name is required")

    if not email:
        errors.append("Email is required")
    elif not EMAIL_PATTERN.fullmatch(email):
        errors.append("Invalid email format")

    if not age_text:
        errors.append("Age is required")
    else:
        try:
            age = int(age_text)
            if not 0 <= age <= 120:
                errors.append("Age must be between 0 and 120")
        except ValueError:
            errors.append("Age must be an integer")

    return errors
