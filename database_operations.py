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


#                                                                      
# BOOK OPERATIONS
#                                                                      

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
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        if cursor.fetchone() is None:
            conn.close()
            return False, f"Book with ID {book_id} not found"
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
            return {
                'book_id': book[0], 'title': book[1],
                'author': book[2], 'published_year': book[3], 'quantity': book[4]
            }
        return None
    except sqlite3.Error as e:
        print(f"Error getting book: {e}")
        return None


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
        return [
            {'book_id': b[0], 'title': b[1], 'author': b[2],
             'published_year': b[3], 'quantity': b[4]}
            for b in books
        ]
    except sqlite3.Error as e:
        print(f"Error getting all books: {e}")
        return []


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
        return [
            {'book_id': b[0], 'title': b[1], 'author': b[2],
             'published_year': b[3], 'quantity': b[4]}
            for b in books
        ]
    except sqlite3.Error as e:
        print(f"Error searching books: {e}")
        return []


def delete_book_from_db(book_id):
    """Delete a book from database"""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        if cursor.fetchone() is None:
            conn.close()
            return False, f"Book with ID {book_id} not found"
        # Block deletion if actively issued
        cursor.execute("""
            SELECT * FROM issues WHERE book_id = ? AND status = 'issued'
        """, (book_id,))
        if cursor.fetchall():
            conn.close()
            return False, "Cannot delete book — it is currently issued to a user."
        cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        conn.commit()
        conn.close()
        return True, "Book deleted successfully"
    except sqlite3.Error as e:
        print(f"Error deleting book: {e}")
        return False, f"Database error: {e}"


#                                                                      
# USER OPERATIONS
#                                                                      

def get_all_users():
    """Get all registered users from the database"""
    try:
        conn = create_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, role FROM users ORDER BY user_id")
        users = [{'user_id': r[0], 'username': r[1], 'role': r[2]}
                 for r in cursor.fetchall()]
        conn.close()
        return users
    except sqlite3.Error as e:
        print(f"Error getting users: {e}")
        return []


def delete_user_from_db(user_id):
    """Delete a user from the database"""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return False, "User not found!"
        if user[0] == 'admin':
            conn.close()
            return False, "Cannot delete admin accounts!"
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True, f"User with ID {user_id} deleted successfully!"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Error deleting user: {e}"


def add_user_with_password(username, password, role='user'):
    """Add a new user with password to the database"""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, "Username already exists."
        cursor.execute("""
            INSERT INTO users (username, role, password)
            VALUES (?, ?, ?)
        """, (username, role, password))
        conn.commit()
        conn.close()
        return True, "User added successfully."
    except sqlite3.Error as e:
        return False, f"Error: {e}"


def verify_user_credentials(username, password):
    """Verify username and password"""
    try:
        conn = create_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        if result is None:
            return False
        return result[0] == password
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def get_user_by_username(username):
    """Return user details as dict by username"""
    try:
        conn = create_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        # ✅ Fixed: select username, role (no email column in your schema)
        cursor.execute("SELECT username, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return {'username': user[0], 'role': user[1]}
        return None
    except sqlite3.Error as e:
        print(f"Error fetching user: {e}")
        return None


#                                                                      
# ISSUE / RETURN OPERATIONS
#                                                                      

def add_issue_record(user_id, book_id):
    """Issue a book to a user"""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        cursor = conn.cursor()

        # Check user exists
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            conn.close()
            return False, f"User ID {user_id} not found"

        # Check book exists and has stock
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        if not book:
            conn.close()
            return False, f"Book ID {book_id} not found"
        if book[4] <= 0:
            conn.close()
            return False, f"Book '{book[1]}' is out of stock!"

        # ✅ Insert WITH status='issued' — required by NOT NULL constraint
        issue_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO issues (user_id, book_id, issue_date, status)
            VALUES (?, ?, ?, 'issued')
        """, (user_id, book_id, issue_date))

        # Reduce book quantity
        cursor.execute("""
            UPDATE books SET quantity = quantity - 1 WHERE book_id = ?
        """, (book_id,))

        conn.commit()
        conn.close()
        return True, "Book issued successfully!"

    except sqlite3.Error as e:
        print(f"SQLite error in add_issue_record: {e}")
        return False, f"Database error: {e}"


def return_book(issue_id):
    """Mark a book as returned"""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        cursor = conn.cursor()

        # ✅ Check by status='issued', not return_date IS NULL
        cursor.execute("""
            SELECT * FROM issues WHERE issue_id = ? AND status = 'issued'
        """, (issue_id,))
        issue = cursor.fetchone()
        if not issue:
            conn.close()
            return False, f"Issue ID {issue_id} not found or already returned"

        return_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            UPDATE issues SET return_date = ?, status = 'returned'
            WHERE issue_id = ?
        """, (return_date, issue_id))

        # Restore book quantity
        cursor.execute("""
            UPDATE books SET quantity = quantity + 1 WHERE book_id = ?
        """, (issue[2],))

        conn.commit()
        conn.close()
        return True, "Book returned successfully!"

    except sqlite3.Error as e:
        print(f"SQLite error in return_book: {e}")
        return False, f"Database error: {e}"


def get_active_issues():
    """Get all currently issued books (status = 'issued')"""
    try:
        conn = create_connection()
        if conn is None:
            return []
        cursor = conn.cursor()

        # ✅ Returns TUPLES so ttk.Treeview in records_page can use values directly
        cursor.execute("""
            SELECT i.issue_id, u.username, b.title, i.issue_date
            FROM issues i
            JOIN users u ON i.user_id = u.user_id
            JOIN books b ON i.book_id = b.book_id
            WHERE i.status = 'issued'
            ORDER BY i.issue_date DESC
        """)
        issues = cursor.fetchall()
        conn.close()
        return issues

    except sqlite3.Error as e:
        print(f"Error getting active issues: {e}")
        return []


#                                                                      
# HISTORY
#                                                                      

def get_all_history():
    """Retrieve all issue history records with user and book details"""
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
        result = []
        for row in records:
            return_date = row[6]
            result.append({
                'issue_id':    row[0],
                'user_id':     row[1],
                'user_name':   row[2],
                'book_name':   row[4],
                'issue_date':  row[5],
                'return_date': return_date if return_date else "N/A",
                'status':      "Returned" if return_date else "Not Returned"
            })
        return result
    except sqlite3.Error as e:
        print(f"Error fetching history: {e}")
        return []


#                                                                      
# PROFILE OPERATIONS
#                                                                      

def update_username(old_username, new_username):
    """Rename a user's username."""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username = ? WHERE username = ?",
                       (new_username, old_username))
        conn.commit()
        conn.close()
        return True, "Username updated successfully."
    except sqlite3.Error as e:
        return False, f"Database error: {e}"


def update_password(username, new_password):
    """Update a user's password."""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?",
                       (new_password, username))
        conn.commit()
        conn.close()
        return True, "Password updated successfully."
    except sqlite3.Error as e:
        return False, f"Database error: {e}"