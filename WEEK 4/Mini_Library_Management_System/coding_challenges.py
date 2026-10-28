"""Ten readable, runnable OOP coding challenge solutions."""
from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    marks: list[float] = field(default_factory=list)

    @property
    def average(self) -> float:
        return sum(self.marks) / len(self.marks) if self.marks else 0.0


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner, self._balance = owner, balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0 or amount > self._balance:
            raise ValueError("Invalid amount or insufficient funds")
        self._balance -= amount


@dataclass
class Employee:
    employee_id: int
    name: str
    department: str


class EmployeeManager:
    def __init__(self) -> None:
        self._employees: dict[int, Employee] = {}

    def add(self, employee: Employee) -> None:
        if employee.employee_id in self._employees:
            raise ValueError("Employee ID already exists")
        self._employees[employee.employee_id] = employee

    def list_all(self) -> list[Employee]:
        return list(self._employees.values())


class Vehicle:
    def __init__(self, brand: str) -> None:
        self.brand = brand

    def move(self) -> str:
        return f"{self.brand} moves"


class Car(Vehicle):
    def move(self) -> str:
        return f"{self.brand} drives on the road"


class Shape:
    def area(self) -> float:
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        if width < 0 or height < 0:
            raise ValueError("Dimensions cannot be negative")
        self.width, self.height = width, height

    def area(self) -> float:
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self.radius = radius

    def area(self) -> float:
        return 3.141592653589793 * self.radius**2


@dataclass
class CartItem:
    name: str
    price: float
    quantity: int = 1


class ShoppingCart:
    def __init__(self) -> None:
        self.items: list[CartItem] = []

    def add(self, item: CartItem) -> None:
        if item.price < 0 or item.quantity <= 0:
            raise ValueError("Price must be non-negative and quantity positive")
        self.items.append(item)

    @property
    def total(self) -> float:
        return sum(i.price * i.quantity for i in self.items)


@dataclass
class Movie:
    title: str
    ratings: list[int] = field(default_factory=list)

    def rate(self, score: int) -> None:
        if not 1 <= score <= 5:
            raise ValueError("Rating must be from 1 to 5")
        self.ratings.append(score)

    @property
    def average_rating(self) -> float:
        return sum(self.ratings) / len(self.ratings) if self.ratings else 0.0


@dataclass
class Patient:
    patient_id: int
    name: str
    notes: list[str] = field(default_factory=list)


class PatientRecords:
    def __init__(self) -> None:
        self._records: dict[int, Patient] = {}

    def add(self, patient: Patient) -> None:
        if patient.patient_id in self._records:
            raise ValueError("Patient ID already exists")
        self._records[patient.patient_id] = patient

    def get(self, patient_id: int) -> Patient:
        return self._records[patient_id]


@dataclass
class SchoolResult:
    student_name: str
    scores: dict[str, float]

    @property
    def total(self) -> float:
        return sum(self.scores.values())

    @property
    def passed(self) -> bool:
        return bool(self.scores) and all(score >= 35 for score in self.scores.values())


@dataclass
class Course:
    title: str
    instructor: str
    students: set[str] = field(default_factory=set)

    def enroll(self, student: str) -> None:
        if not student.strip():
            raise ValueError("Student name is required")
        self.students.add(student)


def main() -> None:
    print("1 Student:", Student("Asha", [80, 90]).average)
    account = BankAccount("Ravi", 100)
    account.deposit(25)
    account.withdraw(10)
    print("2 Bank balance:", account.balance)
    manager = EmployeeManager()
    manager.add(Employee(1, "Mira", "Engineering"))
    print("3 Employees:", len(manager.list_all()))
    print("4 Vehicle:", Car("Tata").move())
    print("5 Rectangle area:", Rectangle(4, 5).area())
    cart = ShoppingCart()
    cart.add(CartItem("Notebook", 30, 2))
    print("6 Cart total:", cart.total)
    movie = Movie("Example Film")
    movie.rate(4)
    movie.rate(5)
    print("7 Movie rating:", movie.average_rating)
    patients = PatientRecords()
    patients.add(Patient(101, "Patient A", ["Routine check"]))
    print("8 Patient:", patients.get(101).name)
    result = SchoolResult("Asha", {"Math": 75, "Science": 82})
    print("9 School result:", result.total, "Pass:", result.passed)
    course = Course("Python OOP", "Instructor")
    course.enroll("Asha")
    print("10 Enrolled:", sorted(course.students))


if __name__ == "__main__":
    main()
