import sqlite3
from datetime import datetime


def create_connection():
    return sqlite3.connect("library.db")


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS books (
        book_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        title          TEXT NOT NULL,
        author         TEXT NOT NULL,
        published_year INTEGER,
        quantity       INTEGER NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        role     TEXT CHECK(role IN ('admin','user')) NOT NULL,
        password TEXT NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS issues (
        issue_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL,
        book_id     INTEGER NOT NULL,
        issue_date  TEXT NOT NULL,
        return_date TEXT,
        status      TEXT CHECK(status IN ('issued','returned')) NOT NULL DEFAULT 'issued',
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )""")
    conn.commit(); conn.close()
    print("✅ Tables created")


def seed_data():
    conn = create_connection(); cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO books (title,author,published_year,quantity) VALUES (?,?,?,?)", [
                    ('Python Basics',   'John Doe',     2020, 5),
                    ('Database Design', 'Jane Smith',   2018, 3),
                    ('Tkinter Guide',   'Alex Ray',     2022, 4),
                    ('Clean Code',      'R. Martin',    2008, 6),
                    ('Data Structures', 'Mark Allen',   2019, 4),
                ])
            print("✅ Sample books added")

        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO users (username,password,role) VALUES (?,?,?)", [
                    ('Manish',   'adminpass', 'admin'),
                    ('Tshering', 'adminpass', 'admin'),
                    ('Hilson',   'userpass1', 'user'),
                    ('Bibek',    'userpass2', 'user'),
                ])
            print("✅ Demo accounts added")
            print("   Admin : Manish   / adminpass")
            print("   Admin : Tshering / adminpass")
            print("   User  : Hilson   / userpass1")
            print("   User  : Bibek    / userpass2")

        cursor.execute("SELECT COUNT(*) FROM issues")
        if cursor.fetchone()[0] == 0:
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO issues (user_id,book_id,issue_date,status) VALUES (3,1,?,'issued')",
                (today,))
            cursor.execute("UPDATE books SET quantity=quantity-1 WHERE book_id=1")
            print("✅ Sample issue added")

        conn.commit()
        print("✅ Database ready!")
    except sqlite3.Error as e:
        print(f"❌ {e}"); conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    create_tables()
    seed_data()