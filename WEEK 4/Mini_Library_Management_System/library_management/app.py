"""Command-line entry point for the Mini Library Management System."""
import json
from pathlib import Path
from .book import BookService
from .exceptions import LibraryError
from .issue import IssueService
from .member import MemberService
from .reports import ReportService
from .storage import JSONStorage


class LibraryApp:
    """Wires services together and provides a small interactive CLI."""

    def __init__(self, data_dir: str | Path | None = None) -> None:
        directory = Path(data_dir) if data_dir else Path(__file__).parent / "data"
        self.books = BookService(JSONStorage(directory / "books.json"))
        self.members = MemberService(JSONStorage(directory / "members.json"))
        self.issues = IssueService(JSONStorage(directory / "issues.json"), self.books, self.members)
        self.reports = ReportService(self.books, self.members, self.issues)

    @staticmethod
    def _print_json(data: object) -> None:
        print(json.dumps(data, indent=2, ensure_ascii=False, default=lambda obj: obj.__dict__))

    def run(self) -> None:
        menu = """
=== MINI LIBRARY MANAGEMENT SYSTEM ===
1. Add book             2. List/search books
3. Register member      4. List members
5. Issue book           6. Return book
7. Available books      8. Borrowed books
9. Top borrowers       10. Fine report
11. Update book        12. Delete book
13. Update member      14. Delete member
0. Exit
"""
        actions = {
            "1": self.add_book, "2": self.list_or_search_books,
            "3": self.register_member, "4": self.list_members,
            "5": self.issue_book, "6": self.return_book,
            "7": lambda: self._print_json(self.reports.available_books()),
            "8": lambda: self._print_json(self.reports.borrowed_books()),
            "9": lambda: self._print_json(self.reports.top_borrowers()),
            "10": lambda: self._print_json(self.reports.fine_report()),
            "11": self.update_book, "12": self.delete_book,
            "13": self.update_member, "14": self.delete_member,
        }
        while True:
            print(menu)
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye!")
                break
            action = actions.get(choice)
            if action is None:
                print("Choose a listed menu option.")
                continue
            try:
                action()
            except (LibraryError, ValueError, KeyError) as exc:
                print(f"Error: {exc}")

    def add_book(self) -> None:
        book = self.books.add(input("Title: "), input("Author: "), int(input("Copies: ")))
        self._print_json(book.to_dict())

    def list_or_search_books(self) -> None:
        query = input("Search text (blank lists all): ").strip()
        books = self.books.search(query) if query else self.books.list_books()
        self._print_json([b.to_dict() | {"available_copies": b.available_copies} for b in books])

    def register_member(self) -> None:
        member = self.members.register(input("Name: "), input("Email: "))
        self._print_json(member.to_dict())

    def list_members(self) -> None:
        self._print_json([m.to_dict() for m in self.members.list_members()])

    def issue_book(self) -> None:
        issue = self.issues.issue_book(int(input("Book ID: ")), int(input("Member ID: ")))
        self._print_json(issue.to_dict())

    def return_book(self) -> None:
        issue = self.issues.return_book(int(input("Issue ID: ")))
        self._print_json(issue.to_dict())

    def update_book(self) -> None:
        book_id = int(input("Book ID: "))
        title = input("New title (blank to keep): ").strip() or None
        author = input("New author (blank to keep): ").strip() or None
        raw = input("New total copies (blank to keep): ").strip()
        self._print_json(self.books.update(book_id, title=title, author=author,
                                           total_copies=int(raw) if raw else None).to_dict())

    def delete_book(self) -> None:
        self.books.delete(int(input("Book ID: ")))
        print("Book deleted.")

    def update_member(self) -> None:
        member_id = int(input("Member ID: "))
        name = input("New name (blank to keep): ").strip() or None
        email = input("New email (blank to keep): ").strip() or None
        active_input = input("Active? y/n/blank to keep: ").strip().lower()
        active = {"y": True, "n": False}.get(active_input) if active_input else None
        self._print_json(self.members.update(member_id, name=name, email=email, active=active).to_dict())

    def delete_member(self) -> None:
        self.members.delete(int(input("Member ID: ")))
        print("Member deleted.")


def main() -> None:
    LibraryApp().run()


if __name__ == "__main__":
    main()
