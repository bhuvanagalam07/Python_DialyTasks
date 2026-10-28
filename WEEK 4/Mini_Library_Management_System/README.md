# Day02 — Python OOP and Mini Library Management System

This folder combines all seven stories into one runnable learning project.

## Files
- `oop_notes.md` — concepts, examples, diagrams, comparisons.
- `oop_examples.py` — encapsulation, inheritance varieties, polymorphism, abstraction, composition and aggregation.
- `magic_methods.py` — requested magic methods and expected output.
- `solid_examples.py` — one practical example for each SOLID principle.
- `coding_challenges.py` — ten OOP coding challenge implementations.
- `library_management/` — complete modular CLI application with JSON storage.

## Start the application
Use Python 3.10 or newer. No packages need to be installed.

```bash
python -m library_management
```

Run the learning examples:

```bash
python oop_examples.py
python magic_methods.py
python solid_examples.py
python coding_challenges.py
```

Run tests:

```bash

Get-ChildItem
Get-ChildItem .\tests
Get-ChildItem .\library_management

Test-Path .\tests\test_library.py

if (-not (Test-Path .\tests\__init__.py)) {
    New-Item .\tests\__init__.py -ItemType File
}

python -m unittest discover -s tests -v
```

## OOP learning map
- Encapsulation: validated Book state and service methods.
- Abstraction: `JSONStorage` hides JSON file details; ABC examples in OOP/SOLID examples.
- Inheritance and polymorphism: learning examples and `Book`/`Member` domain entities.
- Composition/aggregation: issue/report services coordinate reusable services.
- Operator overloading: `magic_methods.py`.
- SOLID: `solid_examples.py`, plus separation between CLI, services, storage, validation and reports.
