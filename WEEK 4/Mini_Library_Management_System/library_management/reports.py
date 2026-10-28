"""Read-only reports assembled from services."""
from collections import Counter
from .book import BookService
from .issue import IssueService
from .member import MemberService


class ReportService:
    """Reports use existing services instead of duplicating storage logic."""

    def __init__(self, books: BookService, members: MemberService,
                 issues: IssueService) -> None:
        self.books, self.members, self.issues = books, members, issues

    def available_books(self) -> list[dict[str, object]]:
        return [{"book_id": b.book_id, "title": b.title, "author": b.author,
                 "available_copies": b.available_copies}
                for b in self.books.list_books() if b.available_copies > 0]

    def borrowed_books(self) -> list[dict[str, object]]:
        book_map = {b.book_id: b for b in self.books.list_books()}
        member_map = {m.member_id: m for m in self.members.list_members()}
        result = []
        for issue in self.issues.list_issues():
            if issue.return_date is None:
                result.append({
                    "issue_id": issue.issue_id,
                    "title": book_map.get(issue.book_id).title if issue.book_id in book_map else "Deleted book",
                    "member": member_map.get(issue.member_id).name if issue.member_id in member_map else "Deleted member",
                    "due_date": issue.due_date,
                })
        return result

    def top_borrowers(self, limit: int = 5) -> list[dict[str, object]]:
        counts = Counter(i.member_id for i in self.issues.list_issues())
        names = {m.member_id: m.name for m in self.members.list_members()}
        return [{"member_id": mid, "name": names.get(mid, "Deleted member"), "borrow_count": count}
                for mid, count in counts.most_common(max(0, limit))]

    def fine_report(self) -> list[dict[str, object]]:
        return [{"issue_id": i.issue_id, "member_id": i.member_id,
                 "book_id": i.book_id, "fine": i.fine}
                for i in self.issues.list_issues() if i.fine > 0]
