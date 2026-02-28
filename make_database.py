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
        role TEXT CHECK(role IN ('admin','user')) NOT NULL
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
                ('Manish', 'admin'),
                ('Tshering', 'admin'),
                ('Hilson', 'user'),
                ('Bibek', 'user')
            ]
            cursor.executemany("INSERT INTO users (username, role) VALUES (?, ?)", users)
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