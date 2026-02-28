from tkinter import *
from function_header_body import header_part, body_part
from database_operations import get_all_books, search_books

root = Tk()
root.title("Library Management System - Available Books")
root.geometry("1220x900")
root.iconbitmap("logo_icon.ico")

header = header_part(root)
body = body_part(root)

# Main container with scrollbar
container = Frame(body, bg="#5D48B8")
container.place(relx=0.5, rely=0.5, anchor=CENTER)

# Canvas with scrollbar
canvas = Canvas(container, bg="#5D48B8", width=850, height=500)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)

# Frame inside the canvas
content_frame = Frame(canvas, bg="#5D48B8")
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Update scrollregion when content changes
def update_scrollregion(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", update_scrollregion)

# Back button at top left (fixed position in container)
back_frame = Frame(container, bg="#a6093d", relief="raised", bd=2)
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

# Title with icon
title_frame = Frame(content_frame, bg="#5D48B8")
title_frame.pack(pady=30)

title_icon = Label(title_frame, text="📚", font=("Arial", 40), 
                   bg="#5D48B8", fg="white")
title_icon.pack(side=LEFT, padx=10)

title_label = Label(title_frame, text="Available Books", 
                   bg="#5D48B8", fg="white", font=("Arial", 24, "bold"))
title_label.pack(side=LEFT)

# Search frame
search_frame = Frame(content_frame, bg="#5D48B8")
search_frame.pack(pady=20)

Label(search_frame, text="Search:", bg="#5D48B8", fg="white", 
      font=("Arial", 12)).pack(side=LEFT, padx=(0, 10))

search_var = StringVar()
search_entry = Entry(search_frame, textvariable=search_var, 
                     font=("Arial", 12), width=40)
search_entry.pack(side=LEFT, padx=(0, 10))

def create_icon_button(parent, text, icon, color, command):
    btn_frame = Frame(parent, bg="white", relief="raised", bd=2)
    btn_frame.pack(side=LEFT, padx=10)
    
    icon_label = Label(btn_frame, text=icon, font=("Arial", 20), 
                       bg="white", fg=color)
    icon_label.pack(side=LEFT, padx=10)
    
    text_label = Label(btn_frame, text=text, font=("Arial", 14, "bold"), 
                       bg="white", fg="black")
    text_label.pack(side=LEFT, padx=(0, 10))
    
    def on_click(e):
        command()
    
    btn_frame.bind("<Button-1>", on_click)
    icon_label.bind("<Button-1>", on_click)
    text_label.bind("<Button-1>", on_click)
    
    def on_enter(e):
        btn_frame.config(bg="lightblue")
        icon_label.config(bg="lightblue")
        text_label.config(bg="lightblue")
    
    def on_leave(e):
        btn_frame.config(bg="white")
        icon_label.config(bg="white")
        text_label.config(bg="white")
    
    btn_frame.bind("<Enter>", on_enter)
    btn_frame.bind("<Leave>", on_leave)
    icon_label.bind("<Enter>", on_enter)
    icon_label.bind("<Leave>", on_leave)
    text_label.bind("<Enter>", on_enter)
    text_label.bind("<Leave>", on_leave)
    
    return btn_frame

# Search button
def search_books_action():
    search_term = search_var.get().strip()
    if search_term:
        books = search_books(search_term)
    else:
        books = get_all_books()
    display_books(books)

search_btn = create_icon_button(search_frame, "Search", "🔍", "#4CAF50", search_books_action)

# Refresh button
def refresh_action():
    search_var.set("")
    books = get_all_books()
    display_books(books)

refresh_btn = create_icon_button(search_frame, "Refresh", "🔄", "#2196F3", refresh_action)

# Table frame
table_frame = Frame(content_frame, bg="#5D48B8")
table_frame.pack(pady=20, padx=20)

#anvas for the table with scrollbar
table_canvas = Canvas(table_frame, bg="#5D48B8", width=800, height=400, highlightthickness=0)
table_canvas.pack(side=LEFT, fill=BOTH, expand=True)

table_scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=table_canvas.yview)
table_scrollbar.pack(side=RIGHT, fill=Y)

table_canvas.configure(yscrollcommand=table_scrollbar.set)

# Frame inside table canvas
inner_table_frame = Frame(table_canvas, bg="#5D48B8")
table_canvas.create_window((0, 0), window=inner_table_frame, anchor="nw")

def update_table_scrollregion(event=None):
    table_canvas.configure(scrollregion=table_canvas.bbox("all"))

inner_table_frame.bind("<Configure>", update_table_scrollregion)

# table headers
headers = ["Book ID", "Book Name", "Author", "Year", "Quantity"]
for i, header in enumerate(headers):
    header_label = Label(inner_table_frame, text=header, bg="#0d1b4c", fg="white", 
                         font=("Arial", 12, "bold"), width=20, relief="ridge", padx=5, pady=5)
    header_label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

# Function to display books in table
def display_books(books):
    # Clear existing rows except headers
    for widget in inner_table_frame.grid_slaves():
        if int(widget.grid_info()["row"]) > 0:
            widget.destroy()
    
    if not books:
        no_books_label = Label(inner_table_frame, text="No books found", bg="#5D48B8", 
                               fg="white", font=("Arial", 14))
        no_books_label.grid(row=1, column=0, columnspan=5, pady=20)
        return
    
    for idx, book in enumerate(books, start=1):
        row_color = "#1a237e" if idx % 2 == 0 else "#283593"
        
        # dictionary keys from database_operations functions
        Label(inner_table_frame, text=book['book_id'], bg=row_color, fg="white", 
              font=("Arial", 11), width=20, relief="ridge", padx=5, pady=5).grid(
                row=idx, column=0, sticky="nsew", padx=1, pady=1)
        
        Label(inner_table_frame, text=book['title'], bg=row_color, fg="white", 
              font=("Arial", 11), width=20, relief="ridge", padx=5, pady=5).grid(
                row=idx, column=1, sticky="nsew", padx=1, pady=1)
        
        Label(inner_table_frame, text=book['author'], bg=row_color, fg="white", 
              font=("Arial", 11), width=20, relief="ridge", padx=5, pady=5).grid(
                row=idx, column=2, sticky="nsew", padx=1, pady=1)
        
        Label(inner_table_frame, text=book['published_year'], bg=row_color, fg="white", 
              font=("Arial", 11), width=20, relief="ridge", padx=5, pady=5).grid(
                row=idx, column=3, sticky="nsew", padx=1, pady=1)
        
        Label(inner_table_frame, text=book['quantity'], bg=row_color, fg="white", 
              font=("Arial", 11), width=20, relief="ridge", padx=5, pady=5).grid(
                row=idx, column=4, sticky="nsew", padx=1, pady=1)
    
    # Configure column weights for proper resizing
    for i in range(5):
        inner_table_frame.grid_columnconfigure(i, weight=1)

# Load and display books 
books = get_all_books()
display_books(books)

# Stats frame
stats_frame = Frame(content_frame, bg="#5D48B8")
stats_frame.pack(pady=20)

def update_stats():
    books = get_all_books()
    total_books = len(books)
    total_quantity = sum(book['quantity'] for book in books)
    
    stats_text = f"Total Books: {total_books} | Total Copies: {total_quantity}"
    stats_label.config(text=stats_text)

stats_label = Label(stats_frame, text="", bg="#5D48B8", fg="white", 
                    font=("Arial", 12, "bold"))
stats_label.pack()

update_stats()

# Instructions
instructions_frame = Frame(content_frame, bg="#5D48B8")
instructions_frame.pack(pady=20)

instructions_text = """Instructions:
1. View all available books in the table above
2. Use the search bar to find specific books
3. Click 'Refresh' to see all books again
4. This is a read-only view - no editing or deleting"""

instructions_label = Label(instructions_frame, text=instructions_text, 
                          bg="#5D48B8", fg="white", font=("Arial", 10), 
                          justify=LEFT)
instructions_label.pack()

# mouse wheel
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# Bind Enter key to search
def on_enter_key(event):
    search_books_action()

search_entry.bind("<Return>", on_enter_key)

# search entry
search_entry.focus_set()

root.mainloop()