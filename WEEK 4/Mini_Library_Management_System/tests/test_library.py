"""Deterministic unit tests using a temporary directory."""
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from library_management.app import LibraryApp
from library_management.exceptions import AvailabilityError, ValidationError


class LibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.app = LibraryApp(Path(self.temp.name))
        self.book = self.app.books.add("Python Basics", "A. Author", 1)
        self.member = self.app.members.register("Test Member", "test@example.com")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_issue_and_return_restores_availability(self) -> None:
        issue = self.app.issues.issue_book(self.book.book_id, self.member.member_id,
                                           today=date(2026, 1, 1))
        self.assertEqual(self.app.books.get(self.book.book_id).available_copies, 0)
        returned = self.app.issues.return_book(issue.issue_id, today=date(2026, 1, 20))
        self.assertEqual(returned.fine, 10.0)  # 5 days overdue * 2
        self.assertEqual(self.app.books.get(self.book.book_id).available_copies, 1)

    def test_cannot_issue_unavailable_book(self) -> None:
        self.app.issues.issue_book(self.book.book_id, self.member.member_id)
        with self.assertRaises(AvailabilityError):
            self.app.issues.issue_book(self.book.book_id, self.member.member_id)

    def test_duplicate_member_email_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self.app.members.register("Another Person", "TEST@example.com")

    def test_cannot_delete_borrowed_book(self) -> None:
        self.app.issues.issue_book(self.book.book_id, self.member.member_id)
        with self.assertRaises(ValidationError):
            self.app.books.delete(self.book.book_id)

    def test_search_and_reports(self) -> None:
        self.assertEqual(len(self.app.books.search("python")), 1)
        self.app.issues.issue_book(self.book.book_id, self.member.member_id)
        self.assertEqual(len(self.app.reports.borrowed_books()), 1)
        self.assertEqual(self.app.reports.top_borrowers()[0]["borrow_count"], 1)


if __name__ == "__main__":
    unittest.main()
