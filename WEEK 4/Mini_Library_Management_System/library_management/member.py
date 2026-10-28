"""Member entity and membership service."""
from dataclasses import asdict, dataclass
from typing import Any
from .exceptions import NotFoundError, ValidationError
from .storage import JSONStorage
from .validator import required_text


@dataclass
class Member:
    member_id: int
    name: str
    email: str
    active: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Member":
        return cls(**data)


class MemberService:
    """Register, update, delete and validate library members."""

    def __init__(self, storage: JSONStorage) -> None:
        self.storage = storage

    def list_members(self) -> list[Member]:
        return [Member.from_dict(row) for row in self.storage.read_all()]

    def get(self, member_id: int) -> Member:
        for member in self.list_members():
            if member.member_id == member_id:
                return member
        raise NotFoundError(f"Member {member_id} was not found.")

    def validate(self, member_id: int) -> Member:
        member = self.get(member_id)
        if not member.active:
            raise ValidationError("Membership is inactive.")
        return member

    def register(self, name: str, email: str) -> Member:
        name, email = required_text(name, "Name"), required_text(email, "Email")
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            raise ValidationError("Enter a valid email address.")
        records = self.storage.read_all()
        if any(row["email"].casefold() == email.casefold() for row in records):
            raise ValidationError("That email is already registered.")
        member_id = max((int(row["member_id"]) for row in records), default=0) + 1
        member = Member(member_id, name, email)
        records.append(member.to_dict())
        self.storage.write_all(records)
        return member

    def update(self, member_id: int, *, name: str | None = None,
               email: str | None = None, active: bool | None = None) -> Member:
        records = self.storage.read_all()
        for row in records:
            if int(row["member_id"]) == member_id:
                if name is not None:
                    row["name"] = required_text(name, "Name")
                if email is not None:
                    email = required_text(email, "Email")
                    if "@" not in email:
                        raise ValidationError("Enter a valid email address.")
                    if any(int(other["member_id"]) != member_id and
                           other["email"].casefold() == email.casefold() for other in records):
                        raise ValidationError("That email is already registered.")
                    row["email"] = email
                if active is not None:
                    row["active"] = bool(active)
                self.storage.write_all(records)
                return Member.from_dict(row)
        raise NotFoundError(f"Member {member_id} was not found.")

    def delete(self, member_id: int) -> None:
        records = self.storage.read_all()
        remaining = [r for r in records if int(r["member_id"]) != member_id]
        if len(remaining) == len(records):
            raise NotFoundError(f"Member {member_id} was not found.")
        self.storage.write_all(remaining)
