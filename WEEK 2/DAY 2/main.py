"""Entry point for the Library Management System."""

from library import (
    add_book,
    display_books,
    search_book,
    borrow_book,
    return_book,
)


def main():
    books = []

    add_book(books, 1, "Python Basics", "John Smith")
    add_book(books, 2, "Learning SQL", "David Lee")
    add_book(books, 3, "Clean Code", "Robert Martin")

    print("\n--- ALL BOOKS ---")
    display_books(books)

    print("\n--- SEARCH BOOK ---")
    found_book = search_book(books, "Python Basics")
    if found_book:
        print(f"Found: {found_book['title']} by {found_book['author']}")
    else:
        print("Book not found.")

    print("\n--- BORROW BOOK ---")
    result = borrow_book(books, 1)
    if result is True:
        print("Book borrowed successfully.")
    elif result is False:
        print("Book is already borrowed.")
    else:
        print("Book ID not found.")

    print("\n--- RETURN BOOK ---")
    result = return_book(books, 1)
    if result is True:
        print("Book returned successfully.")
    elif result is False:
        print("Book is already available.")
    else:
        print("Book ID not found.")

    print("\n--- FINAL BOOK LIST ---")
    display_books(books)


if __name__ == "__main__":
    main()
