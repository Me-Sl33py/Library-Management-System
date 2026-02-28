from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
from datetime import datetime
import sqlite3

# Database connection functions (as in your code)
def create_connection():
    """Create a database connection"""
    try:
        conn = sqlite3.connect("library.db")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def initialize_database():
    """Initialize the database with issues table if it doesn't exist"""
    try:
        conn = create_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                issue_date DATE NOT NULL,
                return_date DATE,
                status TEXT DEFAULT 'issued'
            )
        """)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        return False

def get_all_history():
    """Retrieve all issue history records"""
    try:
        conn = create_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.issue_id, u.username, b.title, i.issue_date, i.return_date, i.status
            FROM issues i
            JOIN users u ON i.user_id = u.user_id
            JOIN books b ON i.book_id = b.book_id
            ORDER BY i.issue_date DESC
        """)
        records = cursor.fetchall()
        conn.close()
        return records
    except sqlite3.Error as e:
        print(f"Error fetching history: {e}")
        return []

# Initialize database
initialize_database()

# Main application window
root = Tk()
root.title("Library Management System - Issue History")
root.geometry("1220x900")
# root.iconbitmap("logo_icon.ico") # Uncomment if you have icon

# Optional: header and body functions (you can replace or remove)
try:
    from function_header_body import header_part, body_part
    header = header_part(root)
    body = body_part(root)
except:
    body = Frame(root, bg="#0d1b4c")
    body.pack(fill=BOTH, expand=True)

# Main container with scrollbars
main_container = Frame(body, bg="#5D48B8")
main_container.pack(fill=BOTH, expand=True)

canvas = Canvas(main_container, bg="#5D48B8", highlightthickness=0)
scrollbar = Scrollbar(main_container, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

content_frame = Frame(canvas, bg="#0d1b4c",highlightthickness=0, borderwidth=0, relief='flat')
container_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

def resize_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(container_window, width=event.width)

content_frame.bind("<Configure>", resize_canvas)
canvas.bind("<Configure>", resize_canvas)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Back button
back_frame = Frame(main_container, bg="#a6093d", relief="raised", bd=2)
back_frame.place(x=20, y=20)

back_icon = Label(back_frame, text="←", font=("Arial", 16), 
                  bg="#a6093d", fg="white")
back_icon.pack(side=LEFT, padx=5)

back_text = Label(back_frame, text="Back to Home", font=("Arial", 12), 
                  bg="#a6093d", fg="white")
back_text.pack(side=LEFT, padx=(0, 5))

def go_back():
    root.destroy()
    import home_page
    home_page.root.mainloop()

def on_back_click(e):
    go_back()

back_frame.bind("<Button-1>", on_back_click)
back_icon.bind("<Button-1>", on_back_click)
back_text.bind("<Button-1>", on_back_click)

def on_back_enter(e):
    back_frame.config(bg="#4fe4ee")
    back_icon.config(bg="#4fe4ee")
    back_text.config(bg="#4fe4ee")

def on_back_leave(e):
    back_frame.config(bg="#a6093d")
    back_icon.config(bg="#a6093d")
    back_text.config(bg="#a6093d")

back_frame.bind("<Enter>", on_back_enter)
back_frame.bind("<Leave>", on_back_leave)
back_icon.bind("<Enter>", on_back_enter)
back_icon.bind("<Leave>", on_back_leave)
back_text.bind("<Enter>", on_back_enter)
back_text.bind("<Leave>", on_back_leave)

# Title
title_frame = Frame(content_frame, bg="#5D48B8")
title_frame.pack(pady=20)

title_icon = Label(title_frame, text="📜", font=("Arial", 40), bg="#5D48B8", fg="white")
title_icon.pack(side=LEFT, padx=10)

title_label = Label(title_frame, text="Issue History", bg="#5D48B8", fg="white", font=("Arial", 24, "bold"))
title_label.pack(side=LEFT)

# Table for history
table_frame = Frame(content_frame, bg="#5D48B8",highlightthickness=0, borderwidth=0, relief='flat')
table_frame.pack(pady=20, padx=20)

canvas_table = Canvas(table_frame, bg="#5D48B8", width=1000,highlightthickness=0, height=500,borderwidth=0, relief='flat')
canvas_table.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar_table_y = Scrollbar(table_frame, orient=VERTICAL, command=canvas_table.yview)
scrollbar_table_x = Scrollbar(table_frame, orient=HORIZONTAL, command=canvas_table.xview)
canvas_table.configure(yscrollcommand=scrollbar_table_y.set, xscrollcommand=scrollbar_table_x.set)
scrollbar_table_y.pack(side=RIGHT, fill=Y)
scrollbar_table_x.pack(side=BOTTOM, fill=X)

inner_table_frame = Frame(canvas_table, bg="#5D48B8")
canvas_table.create_window((0,0), window=inner_table_frame, anchor="nw")

def update_table_scrollregion(event=None):
    canvas_table.configure(scrollregion=canvas_table.bbox("all"))
canvas_table.bind("<Configure>", update_table_scrollregion)
inner_table_frame.bind("<Configure>", update_table_scrollregion)

# Define headers
headers = ["Issue ID", "User Name", "Book Title", "Issue Date", "Return Date", "Status"]
col_widths = [10, 20, 20, 15, 15, 10]  # character widths

# Header row
for i, header in enumerate(headers):
    Label(inner_table_frame, text=header, bg="#0d1b4c", fg="white",
          font=("Arial", 12, "bold"), width=col_widths[i], relief="ridge", padx=5, pady=5).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

# Function to display history
def display_history(records):
    # Clear previous data
    for widget in inner_table_frame.grid_slaves():
        if int(widget.grid_info()["row"]) > 0:
            widget.destroy()
    if not records:
        Label(inner_table_frame, text="No records found", bg="#5D48B8", fg="white", font=("Arial", 14)).grid(row=1, column=0, columnspan=6, pady=20)
        return
    for idx, rec in enumerate(records, start=1):
        row_color = "#1a237e" if idx % 2 == 0 else "#283593"
        for col, value in enumerate(rec):
            Label(inner_table_frame, text=str(value), bg=row_color, fg="white",
                  font=("Arial", 11), width=col_widths[col], relief="ridge", padx=5, pady=5).grid(row=idx, column=col, sticky="nsew", padx=1, pady=1)

# Load data initially
records = get_all_history()
display_history(records)

# Refresh button
def refresh():
    records = get_all_history()
    display_history(records)

refresh_btn = Button(content_frame, text="🔄 Refresh List", font=("Arial", 12, "bold"),
                     bg="#2196F3", fg="white", padx=20, pady=10, command=refresh, cursor="hand2")
refresh_btn.pack(pady=10)

# Run the app
root.mainloop()