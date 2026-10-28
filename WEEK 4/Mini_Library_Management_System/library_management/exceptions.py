"""Domain-specific exceptions."""


class LibraryError(Exception):
    """Base class for expected library application errors."""


class NotFoundError(LibraryError):
    """Raised when a requested record does not exist."""


class ValidationError(LibraryError):
    """Raised when input violates a business rule."""


class AvailabilityError(LibraryError):
    """Raised when a book cannot be issued or returned."""
