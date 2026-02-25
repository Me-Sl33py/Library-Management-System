import sqlite3

def connect():
    return sqlite3.connect("library.db")


#BOOKS 

def add_book(title, author, year, quantity):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, published_year, quantity)
        VALUES (?, ?, ?, ?)
    """, (title, author, year, quantity))
    conn.commit()
    conn.close()

def get_all_books():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def update_book(book_id, title, author, year, quantity):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books
        SET title=?, author=?, published_year=?, quantity=?
        WHERE book_id=?
    """, (title, author, year, quantity, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()


#USERS 

def add_user(username, role):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, role)
        VALUES (?, ?)
    """, (username, role))
    conn.commit()
    conn.close()


#ISSUES

def issue_book(user_id, book_id):
    conn = connect()
    cursor = conn.cursor()

    # Insert into issues table
    cursor.execute("""
        INSERT INTO issues (user_id, book_id, issue_date, status)
        VALUES (?, ?, DATE('now'), 'issued')
    """, (user_id, book_id))

    # Reduce quantity in books table
    cursor.execute("""
        UPDATE books
        SET quantity = quantity - 1
        WHERE book_id = ? AND quantity > 0
    """, (book_id,))

    conn.commit()
    conn.close()


def return_book(issue_id, book_id):
    conn = connect()
    cursor = conn.cursor()

    # Update issue row
    cursor.execute("""
        UPDATE issues
        SET return_date = DATE('now'), status = 'returned'
        WHERE id = ?
    """, (issue_id,))

    # Increase quantity in books table
    cursor.execute("""
        UPDATE books
        SET quantity = quantity + 1
        WHERE book_id = ?
    """, (book_id,))

    conn.commit()
    conn.close()


# GET RECORDS 

def get_records():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT issues.id, users.username, books.title, issues.issue_date, issues.status
        FROM issues
        JOIN users ON issues.user_id = users.user_id
        JOIN books ON issues.book_id = books.book_id
        WHERE issues.status = 'issued'
    """)
    records = cursor.fetchall()
    conn.close()
    return records


def get_history():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.username, books.title, issues.issue_date, issues.return_date, issues.status
        FROM issues
        JOIN users ON issues.user_id = users.user_id
        JOIN books ON issues.book_id = books.book_id
        WHERE issues.status = 'returned'
    """)
    history = cursor.fetchall()
    conn.close()
    return history