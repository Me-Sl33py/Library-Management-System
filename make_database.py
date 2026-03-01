import sqlite3
from datetime import datetime

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
        role TEXT CHECK(role IN ('admin','user')) NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # -------- ISSUES TABLE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issues (
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    print("Tables created successfully ✅")

def seed_data():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check if data already exists to avoid duplicates
        cursor.execute("SELECT COUNT(*) FROM books")
        book_count = cursor.fetchone()[0]
        
        if book_count == 0:
            # Sample Books
            books = [
                ('Python Basics', 'John Doe', 2020, 5),
                ('Database Design', 'Jane Smith', 2018, 3),
                ('Tkinter Guide', 'Alex Ray', 2022, 4)
            ]
            cursor.executemany("INSERT INTO books (title, author, published_year, quantity) VALUES (?, ?, ?, ?)", books)
            print("Sample books added ✅")
        else:
            print(f"Books already exist ({book_count} records)")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Sample Users
            users = [
                ('Manish', 'adminpass', 'admin'),
                ('Tshering', 'adminpass', 'admin'),
                ('Hilson', 'userpass1', 'user'),
                ('Bibek', 'userpass2', 'user')
            ]
            cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", users)
            print("Sample users added ✅")
        else:
            print(f"Users already exist ({user_count} records)")
        
        cursor.execute("SELECT COUNT(*) FROM issues")
        issue_count = cursor.fetchone()[0]
        
        if issue_count == 0:
            # Sample Issue Record - FIXED: Using date('now') instead of DATE('now')
            cursor.execute("""
                INSERT INTO issues (user_id, book_id, issue_date, status)
                VALUES (2, 1, date('now'), 'issued')
            """)
            
            # Reduce quantity for issued book
            cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = 1")
            print("Sample issue record added ✅")
        else:
            print(f"Issues already exist ({issue_count} records)")
        
        conn.commit()
        print("All sample data added successfully ✅")
        
    except sqlite3.Error as e:
        print(f"Error seeding data: {e}")
        conn.rollback()
    finally:
        conn.close()

def verify_tables():
    """Verify that tables exist and have correct structure"""
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        # Check if issues table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='issues'")
        if cursor.fetchone():
            print("✓ Issues table exists")
            
            # Check columns in issues table
            cursor.execute("PRAGMA table_info(issues)")
            columns = cursor.fetchall()
            print("Columns in issues table:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        else:
            print("✗ Issues table does not exist")
            
        # Check other tables
        for table in ['books', 'users']:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print(f"✓ {table.capitalize()} table exists")
            else:
                print(f"✗ {table.capitalize()} table does not exist")
                
    except sqlite3.Error as e:
        print(f"Error verifying tables: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables()
    # seed_data()
    verify_tables()
    print("\n=== Database Setup Complete ===")

import sqlite3
from datetime import datetime

def create_connection():
    return sqlite3.connect("library.db")

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        published_year INTEGER,
        quantity INTEGER NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        username  TEXT NOT NULL UNIQUE,
        role      TEXT CHECK(role IN ('admin','user')) NOT NULL,
        password  TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issues (
        issue_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL,
        book_id     INTEGER NOT NULL,
        issue_date  TEXT NOT NULL,
        return_date TEXT,
        status      TEXT CHECK(status IN ('issued','returned')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )""")

    conn.commit()
    conn.close()
    print("✅ Tables created.")


def seed_data():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # ── Books ─────────────────────────────────────────────────────
        cursor.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone()[0] == 0:
            books = [
                ('Python Basics',       'John Doe',    2020, 5),
                ('Database Design',     'Jane Smith',  2018, 3),
                ('Tkinter Guide',       'Alex Ray',    2022, 4),
                ('Clean Code',          'Robert Martin', 2008, 6),
                ('Data Structures',     'Mark Allen',  2019, 4),
            ]
            cursor.executemany(
                "INSERT INTO books (title, author, published_year, quantity) VALUES (?,?,?,?)",
                books
            )
            print("✅ Sample books added.")
        else:
            print("ℹ️  Books already exist, skipping.")

        # ── Demo Users ────────────────────────────────────────────────
        # Passwords stored as plain text (consistent with verify_user_credentials)
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            users = [
                # (username, role, password)
                ('Manish',   'admin', 'adminpass'),   # admin demo 1
                ('Tshering', 'admin', 'adminpass'),   # admin demo 2
                ('Hilson',   'user',  'userpass1'),   # user demo 1
                ('Bibek',    'user',  'userpass2'),   # user demo 2
            ]
            cursor.executemany(
                "INSERT INTO users (username, role, password) VALUES (?,?,?)",
                users
            )
            print("✅ Demo accounts added.")
            print()
            print("  ┌─────────────────────────────────────────┐")
            print("  │           DEMO ACCOUNTS                 │")
            print("  ├───────────┬────────┬────────────────────┤")
            print("  │ Username  │ Role   │ Password           │")
            print("  ├───────────┼────────┼────────────────────┤")
            print("  │ Manish    │ admin  │ adminpass          │")
            print("  │ Tshering  │ admin  │ adminpass          │")
            print("  │ Hilson    │ user   │ userpass1          │")
            print("  │ Bibek     │ user   │ userpass2          │")
            print("  └───────────┴────────┴────────────────────┘")
        else:
            print("ℹ️  Users already exist, skipping.")

        # ── Sample issue record ───────────────────────────────────────
        cursor.execute("SELECT COUNT(*) FROM issues")
        if cursor.fetchone()[0] == 0:
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                INSERT INTO issues (user_id, book_id, issue_date, status)
                VALUES (3, 1, ?, 'issued')
            """, (today,))
            cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = 1")
            print("✅ Sample issue record added.")
        else:
            print("ℹ️  Issues already exist, skipping.")

        conn.commit()
        print()
        print("✅ Database ready!")

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()


def verify_tables():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        for table in ['books', 'users', 'issues']:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            status = "✓" if cursor.fetchone() else "✗"
            print(f"  {status} {table}")
    finally:
        conn.close()


if __name__ == "__main__":
    print("Setting up database...")
    create_tables()
    seed_data()
    print()
    print("Table check:")
    verify_tables()
    print()
    print("=== Setup Complete ===")