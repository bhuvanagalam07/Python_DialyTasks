"""Book issue/return workflow and fine calculations."""
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from typing import Any
from .book import BookService
from .exceptions import AvailabilityError, NotFoundError, ValidationError
from .member import MemberService
from .storage import JSONStorage
from .validator import positive_int


@dataclass
class Issue:
    issue_id: int
    book_id: int
    member_id: int
    issue_date: str
    due_date: str
    return_date: str | None = None
    fine: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Issue":
        return cls(**data)


class IssueService:
    """Coordinates book and member services (composition)."""

    def __init__(self, storage: JSONStorage, books: BookService,
                 members: MemberService, loan_days: int = 14,
                 fine_per_day: float = 2.0) -> None:
        positive_int(loan_days, "Loan days")
        if fine_per_day < 0:
            raise ValidationError("Fine per day cannot be negative.")
        self.storage, self.books, self.members = storage, books, members
        self.loan_days, self.fine_per_day = loan_days, fine_per_day

    def list_issues(self) -> list[Issue]:
        return [Issue.from_dict(row) for row in self.storage.read_all()]

    def issue_book(self, book_id: int, member_id: int,
                   today: date | None = None) -> Issue:
        self.members.validate(member_id)
        book = self.books.get(book_id)
        if book.available_copies <= 0:
            raise AvailabilityError("No copies of this book are currently available.")
        now = today or date.today()
        records = self.storage.read_all()
        issue_id = max((int(row["issue_id"]) for row in records), default=0) + 1
        issue = Issue(issue_id, book_id, member_id, now.isoformat(),
                      (now + timedelta(days=self.loan_days)).isoformat())
        self.books.change_borrowed(book_id, 1)
        records.append(issue.to_dict())
        self.storage.write_all(records)
        return issue

    def return_book(self, issue_id: int, today: date | None = None) -> Issue:
        records = self.storage.read_all()
        for row in records:
            if int(row["issue_id"]) == issue_id:
                if row["return_date"] is not None:
                    raise AvailabilityError("This issue has already been returned.")
                returned = today or date.today()
                due = date.fromisoformat(row["due_date"])
                overdue_days = max(0, (returned - due).days)
                fine = round(overdue_days * self.fine_per_day, 2)
                self.books.change_borrowed(int(row["book_id"]), -1)
                row["return_date"], row["fine"] = returned.isoformat(), fine
                self.storage.write_all(records)
                return Issue.from_dict(row)
        raise NotFoundError(f"Issue {issue_id} was not found.")

    def calculate_late_days(self, issue: Issue, on_date: date | None = None) -> int:
        end = date.fromisoformat(issue.return_date) if issue.return_date else (on_date or date.today())
        return max(0, (end - date.fromisoformat(issue.due_date)).days)
