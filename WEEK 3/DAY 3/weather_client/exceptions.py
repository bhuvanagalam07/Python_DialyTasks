"""Exception hierarchy: catch ApiError for anything, or a subclass for detail."""


class ApiError(Exception):
    """Base class for all errors raised by this package."""


class ApiTimeoutError(ApiError):
    """Connect/read timeout (after retries were exhausted)."""


class ApiConnectionError(ApiError):
    """Network failure such as DNS or refused connection (after retries)."""


class ApiStatusError(ApiError):
    """Non-2xx HTTP status."""

    def __init__(self, status_code: int, message: str, attempts: int = 1):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.attempts = attempts


class MalformedResponseError(ApiError):
    """2xx response with invalid JSON or an unexpected shape/value."""


class PaginationLimitError(ApiError):
    """Pagination exceeded max_pages or max_items."""
