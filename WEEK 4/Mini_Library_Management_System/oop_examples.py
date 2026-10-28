"""Runnable examples of core OOP concepts, using library-style entities."""
from abc import ABC, abstractmethod


class Book:
    """A catalogue book demonstrating encapsulation."""
    catalogue_label = "Community Library"

    def __init__(self, title: str, copies: int = 1) -> None:
        if not title.strip() or copies < 0:
            raise ValueError("Title is required and copies cannot be negative.")
        self.title = title
        self._copies = copies

    @property
    def copies(self) -> int:
        """Read the number of copies without exposing direct mutation."""
        return self._copies

    def add_copies(self, count: int = 1) -> None:
        if count <= 0:
            raise ValueError("count must be positive")
        self._copies += count

    def __str__(self) -> str:
        return f"{self.title} ({self._copies} copies)"


# Single inheritance
class User:
    """Base user type."""
    def __init__(self, name: str) -> None:
        self.name = name

    def role(self) -> str:
        return "user"


class Member(User):
    """A library member overrides the base role."""
    def role(self) -> str:
        return "member"


# Multilevel inheritance
class PremiumMember(Member):
    def role(self) -> str:
        return "premium member"


# Hierarchical inheritance
class Librarian(User):
    def role(self) -> str:
        return "librarian"


# Multiple inheritance (mixins should remain small and focused)
class Printable:
    def label(self) -> str:
        return "printable"


class Auditable:
    def audit_event(self) -> str:
        return "event recorded"


class AuditedReport(Printable, Auditable):
    pass


# Polymorphism and abstraction
class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        """Send a message through a chosen channel."""


class ConsoleNotifier(Notifier):
    def send(self, message: str) -> str:
        return f"NOTICE: {message}"


def greet(name: str, greeting: str = "Hello") -> str:
    """Simulate method overloading with a default argument."""
    return f"{greeting}, {name}!"


class Shelf:
    """Composition: the shelf creates and owns its inventory list."""
    def __init__(self) -> None:
        self._books: list[Book] = []

    def add(self, book: Book) -> None:
        self._books.append(book)

    def titles(self) -> list[str]:
        return [book.title for book in self._books]


class Library:
    """Aggregation: receives a shelf that can exist independently."""
    def __init__(self, shelf: Shelf) -> None:
        self.shelf = shelf


def main() -> None:
    book = Book("Python OOP", 2)
    book.add_copies()
    print(book)
    print(Member("Asha").role(), PremiumMember("Ravi").role(), Librarian("Mira").role())
    print(AuditedReport().label(), AuditedReport().audit_event())
    print(ConsoleNotifier().send("A book is due tomorrow"))
    print(greet("Asha"), greet("Asha", "Welcome"))
    shelf = Shelf()
    shelf.add(book)
    print("Library titles:", Library(shelf).shelf.titles())


if __name__ == "__main__":
    main()
