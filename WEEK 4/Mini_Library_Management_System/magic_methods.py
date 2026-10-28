"""Examples of Python special methods and expected output."""
from dataclasses import dataclass


@dataclass
class Book:
    title: str
    pages: int

    def __str__(self) -> str:
        return f"{self.title} ({self.pages} pages)"

    def __repr__(self) -> str:
        return f"Book(title={self.title!r}, pages={self.pages!r})"

    def __len__(self) -> int:
        return self.pages

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return (self.title, self.pages) == (other.title, other.pages)

    def __lt__(self, other: "Book") -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.pages < other.pages

    def __gt__(self, other: "Book") -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.pages > other.pages

    def __add__(self, other: "Book") -> int:
        if not isinstance(other, Book):
            return NotImplemented
        return self.pages + other.pages

    def __sub__(self, other: "Book") -> int:
        if not isinstance(other, Book):
            return NotImplemented
        return self.pages - other.pages


def main() -> None:
    a = Book("Python Basics", 120)
    b = Book("Advanced Python", 240)
    print(str(a))
    print(repr(a))
    print(len(a))
    print(a == Book("Python Basics", 120))
    print(a < b, b > a)
    print(a + b)
    print(b - a)


if __name__ == "__main__":
    main()

# Expected output:
# Python Basics (120 pages)
# Book(title='Python Basics', pages=120)
# 120
# True
# True True
# 360
# 120
