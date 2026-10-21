# Python Day 2 — Library Management System

## Objective
Practice modular programming, packages, imports, virtual environments, and dependency files.

## Features
- Add books with an ID, title, and author
- Display all books and their availability
- Search for a book by title
- Borrow a book
- Return a borrowed book
- Prevent duplicate book IDs

## Project structure
```text
python-day2-library/
├── library/
│   ├── __init__.py
│   └── book_operations.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup (Windows PowerShell)
Open PowerShell in the `python-day2-library` folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, you can run the app with the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Run the application
From the project root:

```powershell
python main.py
```

## Important note
Book information is stored in memory, so changes are reset when the program exits. This is a learning project and does not use a database.
