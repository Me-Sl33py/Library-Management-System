import sqlite3
from datetime import datetime

ADMIN_SECRET_KEYS = {"2684", "dust"}


def create_connection():
    try:
        return sqlite3.connect("library.db")
    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

# ── BOOKS ─────────────────────────────────────────────────────────────

def get_all_books():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books ORDER BY title")
        rows = cursor.fetchall(); conn.close()
        return [{'book_id':r[0],'title':r[1],'author':r[2],
                 'published_year':r[3],'quantity':r[4]} for r in rows]
    except sqlite3.Error as e:
        print(e); return []

def search_books(term):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY title",
                       (f'%{term}%', f'%{term}%'))
        rows = cursor.fetchall(); conn.close()
        return [{'book_id':r[0],'title':r[1],'author':r[2],
                 'published_year':r[3],'quantity':r[4]} for r in rows]
    except sqlite3.Error as e:
        print(e); return []

def add_book_to_db(title, author, published_year, quantity):
    try:
        conn = create_connection()
        conn.cursor().execute(
            "INSERT INTO books (title,author,published_year,quantity) VALUES (?,?,?,?)",
            (title, author, published_year, quantity))
        conn.commit(); conn.close(); return True
    except sqlite3.Error as e:
        print(e); return False

def update_book_in_db(book_id, title, author, published_year, quantity):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM books WHERE book_id=?", (book_id,))
        if not cursor.fetchone():
            conn.close(); return False, f"Book ID {book_id} not found"
        cursor.execute(
            "UPDATE books SET title=?,author=?,published_year=?,quantity=? WHERE book_id=?",
            (title, author, published_year, quantity, book_id))
        conn.commit(); conn.close(); return True, "Book updated successfully"
    except sqlite3.Error as e:
        return False, str(e)

def get_book_by_id(book_id):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
        r = cursor.fetchone(); conn.close()
        if r: return {'book_id':r[0],'title':r[1],'author':r[2],
                      'published_year':r[3],'quantity':r[4]}
        return None
    except sqlite3.Error as e:
        print(e); return None

def delete_book_from_db(book_id):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM books WHERE book_id=?", (book_id,))
        if not cursor.fetchone():
            conn.close(); return False, f"Book ID {book_id} not found"
        cursor.execute(
            "SELECT issue_id FROM issues WHERE book_id=? AND return_date IS NULL", (book_id,))
        if cursor.fetchone():
            conn.close(); return False, "Cannot delete — book is currently issued"
        cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
        conn.commit(); conn.close(); return True, "Book deleted successfully"
    except sqlite3.Error as e:
        return False, str(e)

# ── USERS ─────────────────────────────────────────────────────────────

def get_all_users():
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("SELECT user_id,username,role FROM users ORDER BY user_id")
        rows = cursor.fetchall(); conn.close()
        return [{'user_id':r[0],'username':r[1],'role':r[2]} for r in rows]
    except sqlite3.Error as e:
        print(e); return []

def add_user_with_password(username, password, role='user'):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            conn.close(); return False, "Username already exists"
        cursor.execute(
            "INSERT INTO users (username,role,password) VALUES (?,?,?)",
            (username, role, password))
        conn.commit(); conn.close(); return True, "User created successfully"
    except sqlite3.Error as e:
        return False, str(e)

def delete_user_from_db(user_id):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE user_id=?", (user_id,))
        user = cursor.fetchone()
        if not user:
            conn.close(); return False, "User not found"
        if user[0] == 'admin':
            conn.close(); return False, "Cannot delete admin accounts"
        cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        conn.commit(); conn.close(); return True, f"User {user_id} deleted"
    except sqlite3.Error as e:
        return False, str(e)

def verify_user_credentials(username, password):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone(); conn.close()
        return result is not None and result[0] == password
    except sqlite3.Error as e:
        print(e); return False

def get_user_by_username(username):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("SELECT username,role FROM users WHERE username=?", (username,))
        r = cursor.fetchone(); conn.close()
        return {'username':r[0],'role':r[1]} if r else None
    except sqlite3.Error as e:
        print(e); return None

def update_username(old, new):
    try:
        conn = create_connection()
        conn.cursor().execute(
            "UPDATE users SET username=? WHERE username=?", (new, old))
        conn.commit(); conn.close(); return True, "Username updated"
    except sqlite3.Error as e:
        return False, str(e)

def update_password(username, new_password):
    try:
        conn = create_connection()
        conn.cursor().execute(
            "UPDATE users SET password=? WHERE username=?", (new_password, username))
        conn.commit(); conn.close(); return True, "Password updated"
    except sqlite3.Error as e:
        return False, str(e)

# ── ISSUES ────────────────────────────────────────────────────────────

def add_issue_record(user_id, book_id):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        if not cursor.fetchone():
            conn.close(); return False, f"User ID {user_id} not found"
        cursor.execute("SELECT title,quantity FROM books WHERE book_id=?", (book_id,))
        book = cursor.fetchone()
        if not book:
            conn.close(); return False, f"Book ID {book_id} not found"
        if book[1] <= 0:
            conn.close(); return False, f"'{book[0]}' is out of stock"
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO issues (user_id,book_id,issue_date,status) VALUES (?,?,?,'issued')",
            (user_id, book_id, today))
        cursor.execute(
            "UPDATE books SET quantity=quantity-1 WHERE book_id=?", (book_id,))
        conn.commit(); conn.close(); return True, "Book issued successfully!"
    except sqlite3.Error as e:
        return False, str(e)

def return_book(issue_id):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute(
            "SELECT book_id FROM issues WHERE issue_id=? AND return_date IS NULL", (issue_id,))
        issue = cursor.fetchone()
        if not issue:
            conn.close(); return False, f"Issue ID {issue_id} not found or already returned"
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "UPDATE issues SET return_date=?,status='returned' WHERE issue_id=?",
            (today, issue_id))
        cursor.execute(
            "UPDATE books SET quantity=quantity+1 WHERE book_id=?", (issue[0],))
        conn.commit(); conn.close(); return True, "Book returned successfully!"
    except sqlite3.Error as e:
        return False, str(e)

def get_active_issues():
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("""
            SELECT i.issue_id, u.username, b.title, i.issue_date
            FROM issues i
            JOIN users u ON i.user_id=u.user_id
            JOIN books b ON i.book_id=b.book_id
            WHERE i.return_date IS NULL
            ORDER BY i.issue_date DESC""")
        rows = cursor.fetchall(); conn.close()
        return [{'issue_id':r[0],'username':r[1],'book_name':r[2],'issue_date':r[3]}
                for r in rows]
    except sqlite3.Error as e:
        print(e); return []

def get_all_history():
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("""
            SELECT i.issue_id, u.username, b.title,
                   i.issue_date, i.return_date
            FROM issues i
            JOIN users u ON i.user_id=u.user_id
            JOIN books b ON i.book_id=b.book_id
            ORDER BY i.issue_date DESC""")
        rows = cursor.fetchall(); conn.close()
        return [{'issue_id':r[0],'user_name':r[1],'book_name':r[2],
                 'issue_date':r[3],
                 'return_date': r[4] if r[4] else "N/A",
                 'status': "Returned" if r[4] else "Not Returned"}
                for r in rows]
    except sqlite3.Error as e:
        print(e); return []

# ── USER-FACING ───────────────────────────────────────────────────────

def get_user_pending_books(username):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("""
            SELECT i.issue_id, b.title, i.issue_date
            FROM issues i
            JOIN users u ON i.user_id=u.user_id
            JOIN books b ON i.book_id=b.book_id
            WHERE u.username=? AND i.return_date IS NULL
            ORDER BY i.issue_date DESC""", (username,))
        rows = cursor.fetchall(); conn.close()
        return [{'issue_id':r[0],'book_name':r[1],'issue_date':r[2]} for r in rows]
    except sqlite3.Error as e:
        print(e); return []

def get_user_history(username):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("""
            SELECT i.issue_id, b.title, i.issue_date, i.return_date
            FROM issues i
            JOIN users u ON i.user_id=u.user_id
            JOIN books b ON i.book_id=b.book_id
            WHERE u.username=?
            ORDER BY i.issue_date DESC""", (username,))
        rows = cursor.fetchall(); conn.close()
        return [{'issue_id':r[0],'book_name':r[1],'issue_date':r[2],
                 'return_date': r[3] if r[3] else "N/A",
                 'status': "Returned" if r[3] else "Pending"}
                for r in rows]
    except sqlite3.Error as e:
        print(e); return []

def renew_book(username, issue_id):
    try:
        conn = create_connection(); cursor = conn.cursor()
        cursor.execute("""
            SELECT i.issue_id FROM issues i
            JOIN users u ON i.user_id=u.user_id
            WHERE i.issue_id=? AND u.username=? AND i.return_date IS NULL""",
            (issue_id, username))
        if not cursor.fetchone():
            conn.close(); return False, "Issue not found, already returned, or not yours"
        cursor.execute(
            "UPDATE issues SET issue_date=date(issue_date,'+7 days') WHERE issue_id=?",
            (issue_id,))
        conn.commit(); conn.close(); return True, "Renewed! Extended by 7 days."
    except sqlite3.Error as e:
        return False, str(e)