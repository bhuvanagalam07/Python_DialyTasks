"""One small, runnable example for each SOLID principle."""
from abc import ABC, abstractmethod


# S — Single Responsibility: this class only formats a receipt.
class ReceiptFormatter:
    def format(self, member: str, title: str) -> str:
        return f"{member} borrowed {title}"


# O — Open/Closed: add new fine policies by implementing FinePolicy.
class FinePolicy(ABC):
    @abstractmethod
    def calculate(self, overdue_days: int) -> float:
        pass


class StandardFine(FinePolicy):
    def calculate(self, overdue_days: int) -> float:
        return max(0, overdue_days) * 2.0


class StudentFine(FinePolicy):
    def calculate(self, overdue_days: int) -> float:
        return max(0, overdue_days) * 1.0


# L — Liskov Substitution: both policies honor the same non-negative contract.
def quote_fine(policy: FinePolicy, overdue_days: int) -> float:
    return policy.calculate(overdue_days)


# I — Interface Segregation: split read and write capabilities.
class CatalogueReader(ABC):
    @abstractmethod
    def find_title(self, title: str) -> bool:
        pass


class CatalogueWriter(ABC):
    @abstractmethod
    def add_title(self, title: str) -> None:
        pass


class InMemoryCatalogue(CatalogueReader, CatalogueWriter):
    def __init__(self) -> None:
        self._titles: set[str] = set()

    def find_title(self, title: str) -> bool:
        return title.casefold() in self._titles

    def add_title(self, title: str) -> None:
        self._titles.add(title.casefold())


# D — Dependency Inversion: high-level checkout depends on a small abstraction.
class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass


class ConsoleNotifier(Notifier):
    def notify(self, message: str) -> None:
        print(f"Notification: {message}")


class CheckoutService:
    def __init__(self, notifier: Notifier) -> None:
        self._notifier = notifier

    def checkout(self, member: str, title: str) -> str:
        message = f"{member} checked out {title}"
        self._notifier.notify(message)
        return message


def main() -> None:
    print(ReceiptFormatter().format("Asha", "Python"))
    print("Standard fine:", quote_fine(StandardFine(), 3))
    print("Student fine:", quote_fine(StudentFine(), 3))
    catalogue = InMemoryCatalogue()
    catalogue.add_title("Python")
    print("Found:", catalogue.find_title("PYTHON"))
    CheckoutService(ConsoleNotifier()).checkout("Asha", "Python")


if __name__ == "__main__":
    main()
