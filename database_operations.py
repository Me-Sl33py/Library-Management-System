# database_operations.py
import sqlite3
from datetime import datetime

def create_connection():
    """Create a database connection"""
    try:
        conn = sqlite3.connect("library.db")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def add_book_to_db(title, author, published_year, quantity):
    """Add a new book to the database"""
    try:
        conn = create_connection()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, published_year, quantity)
            VALUES (?, ?, ?, ?)
        """, (title, author, published_year, quantity))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error adding book: {e}")
        return False

def update_book_in_db(book_id, title, author, published_year, quantity):
    """Update an existing book in the database"""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        
        cursor = conn.cursor()
        
        # First, check if book exists
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        
        if book is None:
            conn.close()
            return False, f"Book with ID {book_id} not found"
        
        # Update the book
        cursor.execute("""
            UPDATE books 
            SET title = ?, author = ?, published_year = ?, quantity = ?
            WHERE book_id = ?
        """, (title, author, published_year, quantity, book_id))
        
        conn.commit()
        conn.close()
        return True, "Book updated successfully"
    except sqlite3.Error as e:
        print(f"Error updating book: {e}")
        return False, f"Database error: {e}"

def get_book_by_id(book_id):
    """Get book details by ID"""
    try:
        conn = create_connection()
        if conn is None:
            return None
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        conn.close()
        
        if book:
            # Return as dictionary for easier access
            return {
                'book_id': book[0],
                'title': book[1],
                'author': book[2],
                'published_year': book[3],
                'quantity': book[4]
            }
        return None
    except sqlite3.Error as e:
        print(f"Error getting book: {e}")
        return None

def search_books(search_term):
    """Search books by title or author"""
    try:
        conn = create_connection()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ?
            ORDER BY title
        """, (f'%{search_term}%', f'%{search_term}%'))
        
        books = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        result = []
        for book in books:
            result.append({
                'book_id': book[0],
                'title': book[1],
                'author': book[2],
                'published_year': book[3],
                'quantity': book[4]
            })
        return result
    except sqlite3.Error as e:
        print(f"Error searching books: {e}")
        return []

def get_all_books():
    """Get all books from database"""
    try:
        conn = create_connection()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books ORDER BY title")
        books = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        result = []
        for book in books:
            result.append({
                'book_id': book[0],
                'title': book[1],
                'author': book[2],
                'published_year': book[3],
                'quantity': book[4]
            })
        return result
    except sqlite3.Error as e:
        print(f"Error getting all books: {e}")
        return []

def delete_book_from_db(book_id):
    """Delete a book from database"""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        
        cursor = conn.cursor()
        
        # Check if book exists
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        
        if book is None:
            conn.close()
            return False, f"Book with ID {book_id} not found"
        
        # Check if book is currently issued
        cursor.execute("SELECT * FROM issues WHERE book_id = ? AND status = 'issued'", (book_id,))
        active_issues = cursor.fetchall()
        
        if active_issues:
            conn.close()
            return False, "Cannot delete book. It is currently issued to users."
        
        # Delete the book
        cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        conn.commit()
        conn.close()
        return True, "Book deleted successfully"
    except sqlite3.Error as e:
        print(f"Error deleting book: {e}")
        return False, f"Database error: {e}"