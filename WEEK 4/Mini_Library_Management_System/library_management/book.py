"""Book entity and catalogue service."""
from dataclasses import asdict, dataclass
from typing import Any
from .exceptions import NotFoundError, ValidationError
from .storage import JSONStorage
from .validator import positive_int, required_text


@dataclass
class Book:
    book_id: int
    title: str
    author: str
    total_copies: int = 1
    borrowed_copies: int = 0

    @property
    def available_copies(self) -> int:
        """Number of copies currently available."""
        return self.total_copies - self.borrowed_copies

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Book":
        return cls(**data)


class BookService:
    """CRUD and search operations for books."""

    def __init__(self, storage: JSONStorage) -> None:
        self.storage = storage

    def list_books(self) -> list[Book]:
        return [Book.from_dict(row) for row in self.storage.read_all()]

    def get(self, book_id: int) -> Book:
        for book in self.list_books():
            if book.book_id == book_id:
                return book
        raise NotFoundError(f"Book {book_id} was not found.")

    def add(self, title: str, author: str, copies: int = 1) -> Book:
        title, author = required_text(title, "Title"), required_text(author, "Author")
        positive_int(copies, "Copies")
        records = self.storage.read_all()
        new_id = max((int(row["book_id"]) for row in records), default=0) + 1
        book = Book(new_id, title, author, copies)
        records.append(book.to_dict())
        self.storage.write_all(records)
        return book

    def update(self, book_id: int, *, title: str | None = None,
               author: str | None = None, total_copies: int | None = None) -> Book:
        records = self.storage.read_all()
        for row in records:
            if int(row["book_id"]) == book_id:
                borrowed = int(row["borrowed_copies"])
                if title is not None:
                    row["title"] = required_text(title, "Title")
                if author is not None:
                    row["author"] = required_text(author, "Author")
                if total_copies is not None:
                    positive_int(total_copies, "Copies")
                    if total_copies < borrowed:
                        raise ValidationError("Total copies cannot be less than borrowed copies.")
                    row["total_copies"] = total_copies
                self.storage.write_all(records)
                return Book.from_dict(row)
        raise NotFoundError(f"Book {book_id} was not found.")

    def delete(self, book_id: int) -> None:
        records = self.storage.read_all()
        for row in records:
            if int(row["book_id"]) == book_id and int(row["borrowed_copies"]) > 0:
                raise ValidationError("Cannot delete a book while copies are borrowed.")
        remaining = [r for r in records if int(r["book_id"]) != book_id]
        if len(remaining) == len(records):
            raise NotFoundError(f"Book {book_id} was not found.")
        self.storage.write_all(remaining)

    def search(self, query: str) -> list[Book]:
        query = required_text(query, "Search query").casefold()
        return [b for b in self.list_books()
                if query in b.title.casefold() or query in b.author.casefold()]

    def change_borrowed(self, book_id: int, delta: int) -> Book:
        """Internal inventory update used by IssueService."""
        records = self.storage.read_all()
        for row in records:
            if int(row["book_id"]) == book_id:
                updated = int(row["borrowed_copies"]) + delta
                if updated < 0 or updated > int(row["total_copies"]):
                    raise ValidationError("Book availability would become invalid.")
                row["borrowed_copies"] = updated
                self.storage.write_all(records)
                return Book.from_dict(row)
        raise NotFoundError(f"Book {book_id} was not found.")
