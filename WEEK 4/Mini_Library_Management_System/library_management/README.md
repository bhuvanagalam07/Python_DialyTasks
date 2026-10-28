# Mini Library Management System

A small, modular Python CLI application demonstrating OOP fundamentals, inheritance, composition, exceptions, type hints, JSON persistence, reporting, and SOLID-minded design.

## Requirements
- Python 3.10+
- No third-party dependencies

## Run
From the `Day02` directory:

```bash
python -m library_management
```

The app creates/uses JSON files in `library_management/data/`. To keep sample runs isolated, instantiate `LibraryApp(data_dir="some-temp-folder")` from Python.

## Menu features
- Add, update, delete, list and search books; track total/borrowed/available copies.
- Register, update, list and delete members; validate active membership and email.
- Issue and return books; default loan period is 14 days; fine defaults to 2 currency units per overdue day.
- Reports: available books, borrowed books, top borrowers, and fines.

## Architecture
- `book.py`: `Book` entity and catalogue CRUD/search.
- `member.py`: `Member` entity and membership validation.
- `issue.py`: issue/return workflow and fine calculation.
- `reports.py`: reports assembled from services.
- `storage.py`: JSON persistence abstraction.
- `validator.py`: reusable validation.
- `exceptions.py`: domain exceptions.
- `app.py`: dependency wiring and CLI.
- `data/*.json`: initial empty data stores.

## Design notes
`IssueService` composes book/member services; `ReportService` aggregates data from services. Services depend on the `JSONStorage` abstraction rather than file handling scattered throughout the CLI. Domain-specific exceptions make expected failures readable.

JSON files are appropriate for a learning/demo project. For multi-user production deployments, use a transactional database, authentication/authorization, audit logging, backups, and concurrency controls.

## Quick manual test
1. Add a book with 1 copy.
2. Register a member with a valid email.
3. Issue the book using the generated IDs.
4. Check available/borrowed reports.
5. Return using the issue ID and inspect the fine report.
6. Try issuing the same one-copy book again before return; it should be rejected.
