Python Epic 0 — Day 1 Log Analyzer
Objective

Build a Python command-line program that reads a server log, analyzes log levels, extracts errors, and produces a summary report.

Project Structure
python-epic-0/
├── log_analyzer.py
├── sample_server.log
├── errors_only.log
└── README.md

Requirements

Python 3.12

VS Code

Git

Python virtual environment

Log Format

Each valid log line has three parts:

TIMESTAMP LEVEL MESSAGE


Example:

2026-10-05T09:00:00 INFO Request completed successfully
2026-10-05T09:00:01 WARNING High memory usage detected
2026-10-05T09:00:02 ERROR Database connection failed

Features

The analyzer:

Reads sample_server.log.

Counts INFO, WARNING, and ERROR lines.

Finds the five most frequent error messages.

Writes all ERROR lines to errors_only.log.

Prints a summary report.

Detects malformed lines without crashing.

Handles an empty log file.

Handles a log containing only INFO lines.

Handles a missing input file gracefully.

Python Concepts Covered

Variables

Strings

Integers

Dictionaries

Sets

Tuples

Lists

if / else

for loops

Functions

f-strings

File reading

File writing

Exception handling

Counter

Basic defensive programming

Running the Program

Activate the virtual environment and run:

python log_analyzer.py

Testing
Test 1 — Empty file

Create an empty file and temporarily use it as the input.

Expected behavior:

Program does not crash.

All level counts are zero.

No error messages are reported.

Test 2 — INFO-only file

Example:

2026-10-05T09:00:00 INFO Server started
2026-10-05T09:00:01 INFO Request completed
2026-10-05T09:00:02 INFO Health check passed


Expected behavior:

INFO: 3
WARNING: 0
ERROR: 0

Test 3 — Malformed line

Example:

2026-10-05T09:00:00 INFO Server started
THIS IS NOT A VALID LOG LINE
2026-10-05T09:00:02 ERROR Database connection failed


Expected behavior:

Program does not crash.

The malformed line is skipped.

Malformed lines increases by one.

The valid INFO and ERROR lines are still processed.

Completion Criteria

The project is complete when:

log_analyzer.py runs end to end.

sample_server.log contains 500+ lines.

errors_only.log contains only valid ERROR lines.

Empty input does not crash the program.

INFO-only input does not crash the program.

Malformed input does not crash the program.

The trainee can explain every line of log_analyzer.py.

Git contains the Day 1 feature commit.

Git Commit
git add log_analyzer.py sample_server.log errors_only.log README.md
git commit -m "feat(day1): log analyzer with level counts and error extraction"