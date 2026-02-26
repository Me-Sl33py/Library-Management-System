import sqlite3

def create_connection():
    return sqlite3.connect("library.db")

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # -------- BOOKS TABLE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        published_year INTEGER,
        quantity INTEGER NOT NULL
    )
    """)

    # -------- USERS TABLE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        role TEXT CHECK(role IN ('admin','user')) NOT NULL
    )
    """)

    # -------- ISSUES TABLE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL,
        return_date TEXT,
        status TEXT CHECK(status IN ('issued','returned')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
    """)

    conn.commit()
    conn.close()

def seed_data():
    conn = create_connection()
    cursor = conn.cursor()

    #Sample Books
    cursor.execute("INSERT INTO books (title, author, published_year, quantity) VALUES ('Python Basics', 'John Doe', 2020, 5)")
    cursor.execute("INSERT INTO books (title, author, published_year, quantity) VALUES ('Database Design', 'Jane Smith', 2018, 3)")
    cursor.execute("INSERT INTO books (title, author, published_year, quantity) VALUES ('Tkinter Guide', 'Alex Ray', 2022, 4)")

    #Sample Users
    cursor.execute("INSERT INTO users (username, role) VALUES ('Manish', 'admin')")
    cursor.execute("INSERT INTO users (username, role) VALUES ('Tshering', 'admin')")
    cursor.execute("INSERT INTO users (username, role) VALUES ('Hilson', 'user')")
    cursor.execute("INSERT INTO users (username, role) VALUES ('Bibek', 'user')")

    # Sample Issue Record 
    cursor.execute("""
        INSERT INTO issues (user_id, book_id, issue_date, status)
        VALUES (2, 1, DATE('now'), 'issued')
    """)

    # Reduce quantity for issued book
    cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = 1")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    # seed_data()
    print("Database created with sample data ✅")