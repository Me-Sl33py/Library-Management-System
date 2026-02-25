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

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully ✅")