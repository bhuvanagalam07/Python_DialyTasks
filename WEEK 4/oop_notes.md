# Python OOP Fundamentals

## 1. What is Object-Oriented Programming (OOP)?

**Object-Oriented Programming (OOP)** organizes code around **objects**.
An object combines data (attributes) and behavior (methods). For
example, a `Car` object can store its color and speed and provide
actions such as starting or braking.

### Why use OOP?

-   **Organization:** keeps related data and behavior together.
-   **Reusability:** one class can create many objects.
-   **Maintainability:** code is easier to update when responsibilities
    are clear.
-   **Modeling:** classes can represent real-world or business concepts.

Python supports OOP, but not every Python program needs classes.

## 2. Classes and Objects

A **class** is a blueprint defining attributes and methods. An
**object** is a particular instance created from that class.

``` python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} says woof!")


dog1 = Dog("Buddy", 3)
dog2 = Dog("Luna", 5)

print(dog1.name)  # Buddy
print(dog2.name)  # Luna
dog1.bark()       # Buddy says woof!
```

`Dog` is the class. `dog1` and `dog2` refer to separate objects. They
share the behavior defined by the class, but their instance attributes
differ.

### Diagram

``` text
                 Class: Dog
          +-----------------------+
          | Attributes: name, age |
          | Method: bark()        |
          +-----------------------+
                /         \
               / creates   \ creates
              v             v
       Object: dog1     Object: dog2
       name = Buddy     name = Luna
       age = 3          age = 5
```

**Real-world example:** A `BankAccount` class describes what an account
contains and can do. Objects such as `account_a` and `account_b`
represent different accounts with separate balances.

  -----------------------------------------------------------------------
  Class                               Object
  ----------------------------------- -----------------------------------
  Blueprint or definition             Instance created from a class

  Defines available attributes and    Holds its own instance data
  methods                             

  Example: `Dog`                      Example: `Dog("Buddy", 3)`
  -----------------------------------------------------------------------

## 3. Constructors and `__init__`

In everyday Python, `__init__` is called the **initializer**. It runs
after an object has been created and initializes its attributes.
Python's `__new__` method actually creates the object; most classes do
not need to override it.

``` python
class Employee:
    def __init__(self, name, role):
        self.name = name
        self.role = role


employee = Employee("Anu", "Developer")
print(employee.name)  # Anu
print(employee.role)  # Developer
```

When `Employee("Anu", "Developer")` is evaluated, Python creates an
instance and calls `__init__` to initialize it.

Important points: - `__init__` is a special, or *dunder*, method (double
underscores on both sides). - `self` refers to the instance being
initialized. - `__init__` should normally return `None`; it should not
return a different object. - Parameters can have default values.

``` python
class Employee:
    def __init__(self, name, role="Trainee"):
        self.name = name
        self.role = role


print(Employee("Ravi").role)  # Trainee
```

If no custom initialization is required, defining `__init__` is not
mandatory. Python may use an inherited initializer or default behavior.

**Real-world comparison:** The class defines an employee record's
structure; `__init__` fills in starting details such as the employee's
name and role.

## 4. `self`

`self` is the conventional name for the first parameter of an instance
method. It refers to the particular object on which the method is
called. It is a convention rather than a reserved keyword, but use
`self` in normal Python code.

``` python
class Counter:
    def __init__(self, value=0):
        self.value = value

    def increment(self):
        self.value += 1


counter_a = Counter()
counter_b = Counter(10)

counter_a.increment()
print(counter_a.value)  # 1
print(counter_b.value)  # 10
```

When we write `counter_a.increment()`, Python effectively passes
`counter_a` as the method's first argument. `self.value` means the
`value` attribute belonging to this particular instance.

## 5. Instance Variables and Class Variables

**Instance variables** belong to a particular object. They are usually
assigned through `self` and can differ between objects.

**Class variables** are defined in the class body and are shared through
the class unless an instance shadows the name with its own attribute.

``` python
class Employee:
    company = "Example Tech"  # Class variable

    def __init__(self, name, salary):
        self.name = name      # Instance variable
        self.salary = salary  # Instance variable


emp1 = Employee("Anu", 30000)
emp2 = Employee("Ravi", 35000)

print(emp1.name)          # Anu
print(emp2.name)          # Ravi
print(emp1.company)       # Example Tech
print(Employee.company)   # Example Tech
```

### Diagram

``` text
Class: Employee
  company = "Example Tech"
       |                 |
       v                 v
  emp1 object         emp2 object
  name = "Anu"        name = "Ravi"
  salary = 30000      salary = 35000
```

### Common class-variable pitfall

``` python
class Team:
    members = []  # Shared mutable class variable


team_a = Team()
team_b = Team()
team_a.members.append("Anu")

print(team_b.members)  # ['Anu'] — the same shared list
```

If each object needs its own list, initialize it on `self`:

``` python
class Team:
    def __init__(self):
        self.members = []


team_a = Team()
team_b = Team()
team_a.members.append("Anu")

print(team_a.members)  # ['Anu']
print(team_b.members)  # []
```

  -----------------------------------------------------------------------
  Instance variable                   Class variable
  ----------------------------------- -----------------------------------
  Associated with one object          Stored on the class and commonly
                                      shared

  Commonly assigned using             Defined in the class body
  `self.name = value`                 

  Good for name, balance, or employee Good for shared company name or
  ID                                  configuration

  Changing one object's attribute     Mutating a shared mutable class
  normally affects that object        attribute can affect instances
                                      using it
  -----------------------------------------------------------------------

**Note:** `emp1.company = "Other Tech"` creates or updates an instance
attribute on `emp1`; it does not change `Employee.company`. To update
the class attribute, use `Employee.company = "Other Tech"`.

## 6. Instance, Class, and Static Methods

### 6.1 Instance method

An instance method's first parameter is conventionally `self`. It can
read or update the current object's state.

``` python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount
        return self.balance


account = BankAccount("Anu", 100)
print(account.deposit(50))  # 150
```

Use instance methods for actions that depend on a particular object's
data.

### 6.2 Class method

A class method uses the `@classmethod` decorator. Its first parameter is
conventionally `cls`, referring to the class. It can work with
class-level state and is often used as an alternative constructor.

``` python
class Employee:
    company = "Example Tech"

    def __init__(self, name, role):
        self.name = name
        self.role = role

    @classmethod
    def from_text(cls, text):
        name, role = text.split(",")
        return cls(name.strip(), role.strip())


employee = Employee.from_text("Anu, Developer")
print(employee.name)  # Anu
print(employee.role)  # Developer
```

Using `cls(...)` instead of hard-coding `Employee(...)` helps the method
work correctly with subclasses too.

### 6.3 Static method

A static method uses `@staticmethod`. Python does not automatically pass
the instance or class as its first argument. It is a function placed
inside the class because it is logically related to that class.

``` python
class Temperature:
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        return (celsius * 9 / 5) + 32


print(Temperature.celsius_to_fahrenheit(25))  # 77.0
```

Use a static method for a related utility that does not need instance or
class state. If it is not especially related to the class, a
module-level function may be clearer.

### Comparison table

  -----------------------------------------------------------------------
  Method type       Decorator         First parameter   Best suited for
  ----------------- ----------------- ----------------- -----------------
  Instance method   None              `self`            Working with an
                                                        object's data

  Class method      `@classmethod`    `cls`             Class-level
                                                        operations or
                                                        alternative
                                                        constructors

  Static method     `@staticmethod`   No automatic      Related utility
                                      first argument    needing neither
                                                        instance nor
                                                        class state
  -----------------------------------------------------------------------

### One class with all three

``` python
class Employee:
    company = "Example Tech"

    def __init__(self, name):
        self.name = name

    def introduce(self):  # Instance method
        return f"I am {self.name}."

    @classmethod
    def company_name(cls):  # Class method
        return cls.company

    @staticmethod
    def is_valid_name(name):  # Static method
        return isinstance(name, str) and bool(name.strip())


employee = Employee("Anu")
print(employee.introduce())             # I am Anu.
print(Employee.company_name())          # Example Tech
print(Employee.is_valid_name("Ravi"))   # True
```

## 7. `self` vs `cls`

  -----------------------------------------------------------------------
  `self`                              `cls`
  ----------------------------------- -----------------------------------
  Refers to the current instance      Refers to the class

  Used in ordinary instance methods   Used as the first parameter of
                                      class methods

  Accesses instance attributes such   Accesses class attributes such as
  as `self.name`                      `cls.company`

  Standard convention, not a reserved Standard convention, not a reserved
  keyword                             keyword
  -----------------------------------------------------------------------

``` python
class Example:
    category = "Demo"

    def __init__(self, value):
        self.value = value

    def show_value(self):
        return self.value

    @classmethod
    def show_category(cls):
        return cls.category
```

## 8. Object Lifecycle

The **object lifecycle** is the sequence of stages an object passes
through: creation, initialization, use, and eventual cleanup or
destruction.

``` text
Class definition
      |
      v
Object creation (__new__)
      |
      v
Initialization (__init__)
      |
      v
Object is used
(read/update attributes, call methods)
      |
      v
Object becomes unreachable
      |
      v
Object is reclaimed when Python's memory management allows
```

### Main stages

1.  **Class definition:** Python executes the class statement and
    creates a class object.
2.  **Creation:** Calling the class normally invokes `__new__` to create
    an instance.
3.  **Initialization:** Python calls `__init__` to set the instance's
    initial state.
4.  **Use:** The program accesses attributes and calls methods.
5.  **Cleanup and reclamation:** When an object is no longer reachable,
    it may be reclaimed. CPython commonly uses reference counting with a
    cyclic garbage collector, but exact timing should not be relied on
    across Python implementations.

``` python
class FileTracker:
    def __init__(self, filename):
        self.filename = filename
        print(f"Initialized tracker for {self.filename}")

    def describe(self):
        print(f"Tracking: {self.filename}")


tracker = FileTracker("report.csv")
tracker.describe()
del tracker  # Removes this name; it does not guarantee immediate destruction
```

`del tracker` removes the name `tracker`. If another reference still
points to the same object, the object remains accessible. Avoid
depending on `__del__` for important resource cleanup. Use context
managers (`with`) for resources such as files and locks.

``` python
with open("example.txt", "w", encoding="utf-8") as file:
    file.write("Hello")
# The file is closed when the with block exits.
```

## 9. Practical Employee Example

``` python
class Employee:
    company = "Example Tech"
    employee_count = 0

    def __init__(self, employee_id, name, role="Trainee"):
        self.employee_id = employee_id
        self.name = name
        self.role = role
        Employee.employee_count += 1

    def describe(self):
        return f"{self.name} ({self.employee_id}) works as {self.role}."

    @classmethod
    def from_csv_row(cls, row):
        """Create an employee from a simple [id, name, role] row."""
        employee_id, name, role = row
        return cls(employee_id, name, role)

    @staticmethod
    def valid_employee_id(employee_id):
        return isinstance(employee_id, str) and employee_id.strip().isalnum()


employee1 = Employee("E101", "Anu", "Developer")
employee2 = Employee.from_csv_row(["E102", "Ravi", "Tester"])

print(employee1.describe())
print(employee2.describe())
print(Employee.company)
print(Employee.employee_count)
print(Employee.valid_employee_id("E101"))
```

### What this example demonstrates

-   `Employee` is a class.
-   `employee1` and `employee2` are objects.
-   `__init__` initializes each object's data.
-   `self.employee_id`, `self.name`, and `self.role` are instance
    variables.
-   `company` and `employee_count` are class variables.
-   `describe()` is an instance method.
-   `from_csv_row()` is a class method that acts as an alternative
    constructor.
-   `valid_employee_id()` is a static utility method.

**Design note:** This example increments a class counter during
initialization. In a real application, the counter may not equal the
number of employees stored in a database, because objects can be created
and discarded independently of stored records.

## 10. Common Beginner Mistakes

### Mistake 1: Forgetting `self`

Incorrect:

``` python
class Person:
    def greet():
        print("Hello")
```

Correct:

``` python
class Person:
    def greet(self):
        print("Hello")
```

### Mistake 2: Using a class variable for per-object data

If every object needs its own `tasks` list, initialize `self.tasks = []`
inside `__init__` instead of defining a shared `tasks = []` class
variable.

### Mistake 3: Confusing class and instance methods

Use `@classmethod` when the method should receive the class as `cls`. Do
not add the decorator just because a method is written inside a class.

### Mistake 4: Treating `__init__` as the method that creates the object

`__new__` creates the instance; `__init__` initializes it. Most beginner
classes only need to define `__init__`.

### Mistake 5: Assuming `del object_name` always destroys an object immediately

It removes a reference/name. Other references may still exist, and
reclamation timing can vary.

## 11. Quick Revision

-   **Class:** blueprint defining data and behavior.
-   **Object:** an instance of a class.
-   **`__init__`:** initializes a newly created instance.
-   **`self`:** conventional reference to the current instance.
-   **`cls`:** conventional reference to the class in a class method.
-   **Instance variable:** data associated with one object.
-   **Class variable:** data stored on the class and shared when
    accessed without being shadowed.
-   **Instance method:** works naturally with instance state.
-   **Class method:** receives the class; useful for class-level
    operations and alternative constructors.
-   **Static method:** related utility that receives no automatic `self`
    or `cls`.
-   **Object lifecycle:** creation, initialization, use, and eventual
    cleanup/reclamation.

## 12. Practice Questions

1.  What is the difference between a class and an object?
2.  What is the purpose of `__init__`?
3.  Why do instance methods use `self`?
4.  What is the difference between an instance variable and a class
    variable?
5.  What happens if a mutable list is defined as a class variable and
    modified through an instance?
6.  When would you use `@classmethod`?
7.  How is a static method different from an instance method?
8.  What do `self` and `cls` refer to?
9.  What is the difference between object creation and initialization?
10. Does `del my_object` guarantee that the object is immediately
    destroyed?

### Suggested answers

1.  A class defines a structure and behavior; an object is a specific
    instance of it.
2.  It initializes the instance's attributes after creation.
3.  `self` lets the method access or update the current object's
    attributes.
4.  Instance variables belong to an object; class variables are stored
    on the class and commonly shared.
5.  Other instances accessing the same shared list can see the change.
6.  For class-level operations or alternative constructors that should
    work with subclasses.
7.  An instance method receives `self`; a static method receives no
    automatic first argument.
8.  `self` refers to the instance; `cls` refers to the class.
9.  Creation makes the instance; initialization sets its initial state.
10. No. `del` removes a reference; the object may still have other
    references.
