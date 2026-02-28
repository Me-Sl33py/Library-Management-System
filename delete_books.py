from tkinter import *
from function_header_body import header_part, body_part
import tkinter.messagebox as messagebox
from database_operations import get_all_books, delete_book_from_db

root = Tk()
root.title("Library Management System - Delete Book")
root.geometry("1220x900")
root.iconbitmap("logo_icon.ico")

header = header_part(root)
body = body_part(root)

# Main container with scrollbar
container = Frame(body, bg="#5D48B8")
container.place(relx=0.5, rely=0.5, anchor=CENTER)

#canvas with scrollbar
canvas = Canvas(container, bg="#5D48B8", width=800, height=500)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)

#frame inside the canvas
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

title_icon = Label(title_frame, text="🗑️", font=("Arial", 40), 
                   bg="#5D48B8", fg="white")
title_icon.pack(side=LEFT, padx=10)

title_label = Label(title_frame, text="Delete Book", 
                   bg="#5D48B8", fg="white", font=("Arial", 24, "bold"))
title_label.pack(side=LEFT)

# Table frame
table_frame = Frame(content_frame, bg="#0d1b4c")
table_frame.pack(pady=20, padx=20)

# Create table headers
headers = ["Book ID", "Book Name", "Author", "Year", "Quantity"]
for i, header in enumerate(headers):
    Label(table_frame, text=header, bg="#0d1b4c", fg="white", 
          font=("Arial", 12, "bold"), width=15, relief="ridge").grid(row=0, column=i, padx=2, pady=2)

# Function to load and display books
def load_books():
    # Clear existing rows except headers
    for widget in table_frame.grid_slaves():
        if int(widget.grid_info()["row"]) > 0:
            widget.destroy()
    
    books = get_all_books()
    if not books:
        Label(table_frame, text="No books found", bg="#0d1b4c", fg="white", 
              font=("Arial", 12), width=75).grid(row=1, column=0, columnspan=5, pady=10)
        return
        
    for idx, book in enumerate(books, start=1):
        row_color = "#1a237e" if idx % 2 == 0 else "#283593"
        
        # Access dictionary keys instead of numeric indices
        Label(table_frame, text=book['book_id'], bg=row_color, fg="white", 
              font=("Arial", 11), width=15, relief="ridge").grid(row=idx, column=0, padx=2, pady=2)
        Label(table_frame, text=book['title'], bg=row_color, fg="white", 
              font=("Arial", 11), width=15, relief="ridge").grid(row=idx, column=1, padx=2, pady=2)
        Label(table_frame, text=book['author'], bg=row_color, fg="white", 
              font=("Arial", 11), width=15, relief="ridge").grid(row=idx, column=2, padx=2, pady=2)
        Label(table_frame, text=book['published_year'], bg=row_color, fg="white", 
              font=("Arial", 11), width=15, relief="ridge").grid(row=idx, column=3, padx=2, pady=2)
        Label(table_frame, text=book['quantity'], bg=row_color, fg="white", 
              font=("Arial", 11), width=15, relief="ridge").grid(row=idx, column=4, padx=2, pady=2)
        
# Load books initially
load_books()

# Refresh button to reload book list
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

# Button frame for refresh
button_frame = Frame(content_frame, bg="#5D48B8")
button_frame.pack(pady=10)

refresh_btn = create_icon_button(button_frame, "Refresh List", "🔄", "#4CAF50", load_books)

# Delete section frame
delete_frame = Frame(content_frame, bg="#5D48B8")
delete_frame.pack(pady=30)

# Label and entry for deletion
Label(delete_frame, text="Enter Book ID to Delete:", bg="#5D48B8", fg="white", 
      font=("Arial", 14)).pack(side=LEFT, padx=(0, 10))

book_id_entry = Entry(delete_frame, font=("Arial", 14), width=20)
book_id_entry.pack(side=LEFT, padx=(0, 20))

# Delete button
def delete_book():
    book_id = book_id_entry.get().strip()
    
    if not book_id:
        messagebox.showerror("Error", "Please enter a Book ID!")
        return
    
    try:
        book_id_int = int(book_id)
        
        # Show confirmation dialog
        confirm = messagebox.askyesno("Confirm Delete", 
                                      f"Are you sure you want to delete Book ID: {book_id_int}?\n\n"
                                      "This action cannot be undone!")
        
        if confirm:
            success, message = delete_book_from_db(book_id_int)
            
            if success:
                messagebox.showinfo("Success", message)
                book_id_entry.delete(0, END)
                load_books()  # Refresh the list
            else:
                messagebox.showerror("Error", message)
        
    except ValueError:
        messagebox.showerror("Error", "Book ID must be a valid number!")

delete_btn = create_icon_button(delete_frame, "Delete Book", "❌", "#F44336", delete_book)

# Instructions
instructions_frame = Frame(content_frame, bg="#5D48B8")
instructions_frame.pack(pady=20)

instructions_text = """Instructions:
1. View the book list above
2. Enter the Book ID you want to delete
3. Click 'Delete Book' to remove it
4. Click 'Refresh List' to update the table"""

instructions_label = Label(instructions_frame, text=instructions_text, 
                          bg="#5D48B8", fg="white", font=("Arial", 10), 
                          justify=LEFT)
instructions_label.pack()

# Set focus to entry
book_id_entry.focus_set()

# Add mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

root.mainloop()