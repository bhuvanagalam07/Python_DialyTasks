# Python OOP Fundamentals — Day02

## Goal
Build reusable, maintainable Python applications by modeling domain concepts as objects. This project uses a Library Management System as its running example.

## Class and object
A **class** defines data and behavior; an **object** is an instance of that class.

```python
class Book:
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author

book = Book("Clean Code", "Robert C. Martin")
print(book.title)
```

Real-world mapping: `Book` is a blueprint; each physical/catalogued book is an object.

## Constructor, `self`, and object lifecycle
- `__init__` initializes an already-created object.
- `self` refers to the current instance and is used to read/write instance attributes.
- Lifecycle: create instance → initialize via `__init__` → use object → references disappear → garbage collector may reclaim it. `__del__` exists, but deterministic cleanup should use context managers rather than relying on it.

## Instance variables vs class variables
- Instance variable: belongs to one object (`self.title`).
- Class variable: shared by instances (`Book.catalogue_name`). Avoid mutable class-level values for per-object state.

## Instance, class, and static methods
- Instance method: receives `self`; works with one object.
- Class method: receives `cls`; often provides alternate constructors or class-wide behavior.
- Static method: receives neither automatically; groups a related utility with the class.

```python
class Member:
    membership_type = "standard"

    def __init__(self, name: str) -> None:
        self.name = name

    def display_name(self) -> str:
        return self.name

    @classmethod
    def standard(cls, name: str) -> "Member":
        return cls(name)

    @staticmethod
    def valid_name(name: str) -> bool:
        return bool(name.strip())
```

## Four pillars of OOP
1. **Encapsulation** — keep state and rules together; expose safe methods. Python uses conventions such as `_balance` and name-mangling with `__balance`, not strict access modifiers.
2. **Abstraction** — expose essential operations while hiding implementation details. `abc.ABC` and `@abstractmethod` can define required behavior.
3. **Inheritance** — create a specialized class from a base class to reuse/extend behavior.
4. **Polymorphism** — use a common interface with different implementations, e.g. different report exporters implement `export()`.

## Inheritance and polymorphism
```python
class User:
    def describe(self) -> str:
        return "Library user"

class Librarian(User):
    def describe(self) -> str:
        return "Library administrator"

for user in (User(), Librarian()):
    print(user.describe())
```
Output:
```text
Library user
Library administrator
```

## Composition vs aggregation
- **Composition**: a strong “has-a” relationship; the containing object owns/creates a component. Example: a `Library` owns its in-memory catalogue service.
- **Aggregation**: a looser relationship; objects can exist independently and are passed into a container. Example: a report service receives an existing repository.
- **Inheritance** is “is-a”; composition is usually preferred when behavior can be assembled instead of inherited.

## Diagram
```text
LibraryApp
  ├── BookService ──> JSONStorage
  ├── MemberService ──> JSONStorage
  ├── IssueService ──> BookService + MemberService
  └── ReportService ──> BookService + MemberService + IssueService

Book / Member / Issue are domain entities.
```

## Related concepts at a glance
| Concept A | Concept B | Difference |
|---|---|---|
| Class | Object | Blueprint vs instance |
| Instance variable | Class variable | Per-object vs shared |
| `self` | `cls` | Current object vs current class |
| `@classmethod` | `@staticmethod` | Receives class vs no implicit first argument |
| Inheritance | Composition | “is-a” vs “has-a” |
| Encapsulation | Abstraction | Protect internal state vs simplify visible interface |
| Overriding | Overloading | Replace inherited behavior vs accept different call signatures; Python commonly uses defaults/`*args` rather than signature-based overloads |

## Magic methods and operator overloading
Special methods let objects participate in built-in operations: `__str__` for user display, `__repr__` for developer representation, `__len__` for `len(x)`, comparison methods for sorting/comparison, and `__add__`/`__sub__` for operators. Implement only operations that have clear domain meaning.

## SOLID
- **S**ingle Responsibility: one reason to change per class/module.
- **O**pen/Closed: extend behavior without editing stable code.
- **L**iskov Substitution: subclasses honor the promises of their base class.
- **I**nterface Segregation: small focused interfaces are better than one giant interface.
- **D**ependency Inversion: high-level logic depends on abstractions, not concrete low-level details.

## Production-minded practices in this project
Type hints, docstrings, validation, domain-specific exceptions, JSON persistence, separation of services/storage/CLI, deterministic tests, and clear names. JSON is suitable for a learning project/small local tool; a concurrent or high-volume service should use a database with transactions and access control.
