from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
from datetime import datetime
import sqlite3

root = Tk()
root.title("Library Management System - Book Records")
root.geometry("1220x900")
root.iconbitmap("logo_icon.ico")

# Database connection
def create_connection():
    """Create a database connection"""
    try:
        conn = sqlite3.connect("library.db")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# Check if issues table exists 
def initialize_database():
    """Initialize the database with issues table if it doesn't exist"""
    try:
        conn = create_connection()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        
        #issues table 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                issue_date DATE NOT NULL,
                return_date DATE,
                status TEXT DEFAULT 'issued',
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (book_id) REFERENCES books (book_id)
            )
        """)
        
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        return False

def add_issue_record(user_id, book_id):
    """Add a new issue record to database"""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return False, f"User with ID {user_id} not found"
        
        # Check if book exists and is available
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        if not book:
            conn.close()
            return False, f"Book with ID {book_id} not found"
        
        # Check stock
        if len(book) > 4 and book[4] <= 0:
            conn.close()
            return False, f"Book '{book[1]}' is out of stock!"
        
        # Insert issue record
        issue_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO issues (user_id, book_id, issue_date, status)
            VALUES (?, ?, ?, ?)
        """, (user_id, book_id, issue_date, 'issued'))
        
        # Update book quantity
        cursor.execute("""
            UPDATE books SET quantity = quantity - 1 
            WHERE book_id = ?
        """, (book_id,))
        
        conn.commit()
        conn.close()
        return True, "Book issued successfully!"
        
    except sqlite3.Error as e:
        print(f"Error issuing book: {e}")
        return False, f"Database error: {e}"

def return_book(issue_id):
    """Return a book (mark as returned)"""
    try:
        conn = create_connection()
        if conn is None:
            return False, "Database connection failed"
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM issues 
            WHERE issue_id = ? AND status = 'issued'
        """, (issue_id,))
        issue = cursor.fetchone()
        if not issue:
            conn.close()
            return False, f"Issue ID {issue_id} not found or already returned"
        
        return_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            UPDATE issues 
            SET return_date = ?, status = 'returned'
            WHERE issue_id = ?
        """, (return_date, issue_id))
        
        cursor.execute("""
            UPDATE books SET quantity = quantity + 1 
            WHERE book_id = ?
        """, (issue[2],))
        
        conn.commit()
        conn.close()
        return True, "Book returned successfully!"
    except sqlite3.Error as e:
        print(f"Error returning book: {e}")
        return False, f"Database error: {e}"

def get_active_issues():
    """Get all active issues"""
    try:
        conn = create_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='issues'")
        if not cursor.fetchone():
            conn.close()
            return []
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

# Initialize database
initialize_database()

# UI Design
try:
    from function_header_body import header_part, body_part
    header = header_part(root)
    body = body_part(root)
except:
    body = Frame(root, bg="#0d1b4c")
    body.pack(fill=BOTH, expand=True)

# Create main container with scrollbar
main_container = Frame(body, bg="#5D48B8")
main_container.pack(fill=BOTH, expand=True)

# Create a canvas and scrollbar
canvas = Canvas(main_container, bg="#5D48B8", highlightthickness=0)
scrollbar = Scrollbar(main_container, orient=VERTICAL, command=canvas.yview)

# Create a frame inside the canvas for all content
container = Frame(canvas, bg="#0d1b4c")

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

# Put the container frame in the canvas
container_window = canvas.create_window((0, 0), window=container, anchor="nw")

def configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(container_window, width=event.width)

container.bind("<Configure>", configure_scroll_region)
canvas.bind("<Configure>", configure_scroll_region)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# Add a back button at top-left
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
title_frame = Frame(container, bg="#5D48B8")
title_frame.pack(pady=20)

title_icon = Label(title_frame, text="📋", font=("Arial", 40), bg="#5D48B8", fg="white")
title_icon.pack(side=LEFT, padx=10)

title_label = Label(title_frame, text="Book Records", bg="#5D48B8", fg="white", font=("Arial", 24, "bold"))
title_label.pack(side=LEFT)

# Create form row function
def create_form_row(parent, icon, label_text, row):
    label_frame = Frame(parent, bg="#5D48B8")
    label_frame.grid(row=row, column=0, padx=20, pady=15, sticky="w")
    icon_label = Label(label_frame, text=icon, font=("Arial", 16), bg="#5D48B8", fg="white")
    icon_label.pack(side=LEFT, padx=(0,10))
    Label(label_frame, text=label_text, bg="#5D48B8", fg="white", font=("Arial", 14)).pack(side=LEFT)
    entry = Entry(parent, font=("Arial", 14), width=40)
    entry.grid(row=row, column=1, padx=20, pady=15)
    return entry

# Create button function
def create_button(parent, text, icon, color, command):
    btn = Button(parent, text=f"{icon} {text}", font=("Arial", 12, "bold"),
                 bg=color, fg="white", padx=20, pady=10,
                 command=command, cursor="hand2")
    return btn

# Issue Book Section
issue_frame = Frame(container, bg="#5D48B8", relief="groove", bd=2)
issue_frame.pack(pady=20, padx=20, fill=X)

Label(issue_frame, text="📖 Issue Book", bg="#5D48B8", fg="white",
      font=("Arial", 16, "bold")).pack(pady=10)

issue_form_frame = Frame(issue_frame, bg="#5D48B8")
issue_form_frame.pack(pady=10)

issue_user_entry = create_form_row(issue_form_frame, "👤", "User ID:", 0)
issue_book_entry = create_form_row(issue_form_frame, "📕", "Book ID:", 1)

def on_issue_click():
    user_id = issue_user_entry.get().strip()
    book_id = issue_book_entry.get().strip()
    if not user_id or not book_id:
        messagebox.showerror("Error", "Please enter both User ID and Book ID!")
        return
    try:
        user_id_int = int(user_id)
        book_id_int = int(book_id)
        success, message = add_issue_record(user_id_int, book_id_int)
        if success:
            messagebox.showinfo("Success", message)
            issue_user_entry.delete(0, END)
            issue_book_entry.delete(0, END)
            refresh_issues()
        else:
            messagebox.showerror("Error", message)
    except ValueError:
        messagebox.showerror("Error", "User ID and Book ID must be numbers!")

issue_btn = create_button(issue_frame, "Issue Book", "📤", "#4CAF50", on_issue_click)
issue_btn.pack(pady=10)

# Return Book Section
return_frame = Frame(container, bg="#5D48B8", relief="groove", bd=2)
return_frame.pack(pady=20, padx=20, fill=X)

Label(return_frame, text="📥 Return Book", bg="#5D48B8", fg="white",
      font=("Arial", 16, "bold")).pack(pady=10)

return_form_frame = Frame(return_frame, bg="#5D48B8")
return_form_frame.pack(pady=10)

return_issue_entry = create_form_row(return_form_frame, "🆔", "Issue ID:", 0)

def on_return_click():
    issue_id = return_issue_entry.get().strip()
    if not issue_id:
        messagebox.showerror("Error", "Please enter Issue ID!")
        return
    try:
        issue_id_int = int(issue_id)
        confirm = messagebox.askyesno("Confirm Return", f"Return book for Issue ID {issue_id_int}?")
        if confirm:
            success, message = return_book(issue_id_int)
            if success:
                messagebox.showinfo("Success", message)
                return_issue_entry.delete(0, END)
                refresh_issues()
            else:
                messagebox.showerror("Error", message)
    except ValueError:
        messagebox.showerror("Error", "Issue ID must be a number!")

return_btn = create_button(return_frame, "Return Book", "📥", "#FF5722", on_return_click)
return_btn.pack(pady=10)

# Active Issues Section
active_frame = Frame(container, bg="#5D48B8", relief="groove", bd=2)
active_frame.pack(pady=20, padx=20, fill=X)

Label(active_frame, text="📊 Active Issues", bg="#5D48B8", fg="white",
      font=("Arial", 16, "bold")).pack(pady=10)

# Treeview for active issues
tree_frame = Frame(active_frame, bg="#5D48B8")
tree_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

tree = ttk.Treeview(tree_frame, columns=("Issue ID", "User", "Book Title", "Issue Date"), show="headings", height=8)
tree.heading("Issue ID", text="Issue ID")
tree.heading("User", text="User")
tree.heading("Book Title", text="Book Title")
tree.heading("Issue Date", text="Issue Date")
tree.column("Issue ID", width=100, anchor="center")
tree.column("User", width=200, anchor="center")
tree.column("Book Title", width=300, anchor="center")
tree.column("Issue Date", width=150, anchor="center")
vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
tree.pack(side=LEFT, fill=BOTH, expand=True)
vsb.pack(side=RIGHT, fill=Y)
hsb.pack(side=BOTTOM, fill=X)

# Style for treeview
style = ttk.Style()
style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
style.map('Treeview', background=[('selected', '#5D48B8')])

def refresh_issues():
    for item in tree.get_children():
        tree.delete(item)
    issues = get_active_issues()
    if not issues:
        tree.insert("", "end", values=("No active issues", "", "", ""))
    else:
        for issue in issues:
            tree.insert("", "end", values=issue)

# Refresh button
refresh_btn = create_button(active_frame, "Refresh List", "🔄", "#2196F3", refresh_issues)
refresh_btn.pack(pady=10)

# Initial load
refresh_issues()

# Back button at top-left
back_frame = Frame(container, bg="#a6093d", relief="raised", bd=2)
back_frame.place(x=20, y=20)
back_icon = Label(back_frame, text="←", font=("Arial", 16), bg="#a6093d", fg="white")
back_icon.pack(side=LEFT, padx=5)
back_text = Label(back_frame, text="Back to Home", font=("Arial", 12), bg="#a6093d", fg="white")
back_text.pack(side=LEFT, padx=(0,5))
def go_back():
    root.destroy()
    # import home_page  # Uncomment if you have a home page script
    # home_page.root.mainloop()
def on_back_click(e): go_back()
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

root.mainloop()