"""Operations for managing library books."""


def add_book(books, book_id, title, author):
    """Add a new book to the collection."""
    if any(book["id"] == book_id for book in books):
        raise ValueError(f"A book with ID {book_id} already exists.")

    book = {
        "id": book_id,
        "title": title,
        "author": author,
        "available": True,
    }
    books.append(book)
    return book


def display_books(books):
    """Display all books and their availability."""
    if not books:
        print("No books found.")
        return

    for book in books:
        status = "Available" if book["available"] else "Borrowed"
        print(
            f"ID: {book['id']} | Title: {book['title']} | "
            f"Author: {book['author']} | Status: {status}"
        )


def search_book(books, title):
    """Find a book by its title, ignoring letter case."""
    for book in books:
        if book["title"].casefold() == title.casefold():
            return book
    return None


def borrow_book(books, book_id):
    """Borrow a book by ID. Return True, False, or None."""
    for book in books:
        if book["id"] == book_id:
            if not book["available"]:
                return False
            book["available"] = False
            return True
    return None


def return_book(books, book_id):
    """Return a borrowed book by ID. Return True, False, or None."""
    for book in books:
        if book["id"] == book_id:
            if book["available"]:
                return False
            book["available"] = True
            return True
    return None
