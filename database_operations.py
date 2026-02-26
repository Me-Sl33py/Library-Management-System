# database_operation.py - Add these functions

import sqlite3

def connect_db():
    """Connect to the SQLite database"""
    return sqlite3.connect("library.db")

def add_book_to_db(title, author, year, quantity):
    """Add a new book to the database"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, published_year, quantity)
            VALUES (?, ?, ?, ?)
        """, (title, author, year, quantity))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding book: {str(e)}")
        return False

def update_book_in_db(book_id, title, author, year, quantity):
    """Update an existing book in the database"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE books 
            SET title=?, author=?, published_year=?, quantity=?
            WHERE book_id=?
        """, (title, author, year, quantity, book_id))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
    except Exception as e:
        print(f"Error updating book: {str(e)}")
        return False

def get_book_by_id(book_id):
    """Get book details by ID"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
        book = cursor.fetchone()
        conn.close()
        return book
    except Exception as e:
        print(f"Error fetching book: {str(e)}")
        return None