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
    
def get_all_users():
    """Get all registered users from the database"""
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, role 
            FROM users 
            ORDER BY user_id
        ''')
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'user_id': row[0],
                'username': row[1],
                'role': row[2]
            })
        
        conn.close()
        return users
        
    except Exception as e:
        print(f"Error getting users: {e}")
        return []

def delete_user_from_db(user_id):
    """Delete a user from the database"""
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # First check if user exists
        cursor.execute('SELECT role FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return False, "User not found!"
        
        # Check if user is admin
        if user[0] == 'admin':
            conn.close()
            return False, "Cannot delete admin accounts!"
        
        # Delete the user
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        return True, f"User with ID {user_id} deleted successfully!"
        
    except Exception as e:
        conn.close()
        return False, f"Error deleting user: {str(e)}"

def get_all_history():
    """Retrieve all issue history records with user and book details."""
    try:
        conn = create_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                issues.issue_id,
                issues.user_id,
                users.username,
                issues.book_id,
                books.title,
                issues.issue_date,
                issues.return_date
            FROM issues
            JOIN users ON issues.user_id = users.user_id
            JOIN books ON issues.book_id = books.book_id
            ORDER BY issues.issue_date DESC
        """)
        records = cursor.fetchall()
        conn.close()

        # Format data into list of dicts
        result = []
        for row in records:
            issue_id = row[0]
            user_id = row[1]
            user_name = row[2]
            book_id = row[3]
            book_name = row[4]
            issue_date = row[5]
            return_date = row[6]
            status = "Returned" if return_date else "Not Returned"

            result.append({
                'issue_id': issue_id,
                'user_id': user_id,
                'user_name': user_name,
                'book_name': book_name,
                'issue_date': issue_date,
                'return_date': return_date if return_date else "N/A",
                'status': status
            })

        return result

    except sqlite3.Error as e:
        print(f"Error fetching history: {e}")
        return []