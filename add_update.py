from tkinter import *
from function_header_body import header_part, body_part, hover_color
import tkinter.messagebox as messagebox
from database_operations import add_book_to_db, update_book_in_db, get_book_by_id  # Import database functions

root = Tk()
root.title("Library Management System - Add/Update Book")
root.geometry("1220x900")
root.iconbitmap("logo_icon.ico")

header = header_part(root)
body = body_part(root)

# Main container
container = Frame(body, bg="#5D48B8", width=800, height=500)
container.place(relx=0.5, rely=0.5, anchor=CENTER)
container.pack_propagate(False)

# Title with icon
title_frame = Frame(container, bg="#5D48B8")
title_frame.pack(pady=30)

title_icon = Label(title_frame, text="📖", font=("Arial", 40), 
                   bg="#0d1b4c", fg="white")
title_icon.pack(side=LEFT, padx=10)

title_label = Label(title_frame, text="Add / Update Book", 
                   bg="#5D48B8", fg="white", font=("Arial", 24, "bold"))
title_label.pack(side=LEFT)

# Form frame
form_frame = Frame(container, bg="#0d1b4c")
form_frame.pack(pady=20)

# Labels and Entries with icons
def create_form_row(icon, label_text, row):
    # Icon and label frame
    label_frame = Frame(form_frame, bg="#0d1b4c")
    label_frame.grid(row=row, column=0, padx=20, pady=15, sticky="w")
    
    icon_label = Label(label_frame, text=icon, font=("Arial", 16), 
                       bg="#0d1b4c", fg="white")
    icon_label.pack(side=LEFT, padx=(0, 10))
    
    Label(label_frame, text=label_text, bg="#5D48B8", fg="white", 
          font=("Arial", 14)).pack(side=LEFT)
    
    # Entry field
    entry = Entry(form_frame, font=("Arial", 14), width=40)
    entry.grid(row=row, column=1, padx=20, pady=15)
    return entry

# Create form fields with icons
book_name_entry = create_form_row("📕", "Book Name:", 0)
author_entry = create_form_row("✍️", "Author:", 1)
year_entry = create_form_row("📅", "Published Year:", 2)
quantity_entry = create_form_row("🔢", "Quantity:", 3)

# Buttons frame
button_frame = Frame(container, bg="#5D48B8")
button_frame.pack(pady=30)

def add_book():
    name = book_name_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    quantity = quantity_entry.get()
    
    if not all([name, author, year, quantity]):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        year = int(year)
        quantity = int(quantity)
        if year < 0 or quantity < 0:
            messagebox.showerror("Error", "Year and Quantity must be positive!")
            return
        
        # Call database function to add book
        if add_book_to_db(name, author, year, quantity):
            messagebox.showinfo("Success", "Book added successfully to database!")
            
            # Clear fields
            book_name_entry.delete(0, END)
            author_entry.delete(0, END)
            year_entry.delete(0, END)
            quantity_entry.delete(0, END)
        else:
            messagebox.showerror("Error", "Failed to add book to database!")
        
    except ValueError:
        messagebox.showerror("Error", "Year and Quantity must be numbers!")

def update_book():
    # For update, we need book ID - you might want to add a Book ID field
    # For now, let's use book name to find and update
    name = book_name_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    quantity = quantity_entry.get()
    
    if not all([name, author, year, quantity]):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        year = int(year)
        quantity = int(quantity)
        if year < 0 or quantity < 0:
            messagebox.showerror("Error", "Year and Quantity must be positive!")
            return
        
        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Update", 
                                       f"Update book '{name}' by {author}?\nYear: {year}, Quantity: {quantity}")
        if confirm:
            # Here you would need book_id to update specific book
            # For now, this shows how to call the update function
            messagebox.showinfo("Info", "Update function requires Book ID. Please add a Book ID field.")
            # Example: update_book_in_db(book_id, name, author, year, quantity)
        
    except ValueError:
        messagebox.showerror("Error", "Year and Quantity must be numbers!")

# Create buttons with icons
def create_icon_button(parent, text, icon, color, command):
    btn_frame = Frame(parent, bg="white", relief="raised", bd=2)
    btn_frame.pack(side=LEFT, padx=10)
    
    icon_label = Label(btn_frame, text=icon, font=("Arial", 20), 
                       bg="white", fg=color)
    icon_label.pack(side=LEFT, padx=10)
    
    text_label = Label(btn_frame, text=text, font=("Arial", 14, "bold"), 
                       bg="white", fg="black")
    text_label.pack(side=LEFT, padx=(0, 10))
    
    # Bind click events
    def on_click(e):
        command()
    
    btn_frame.bind("<Button-1>", on_click)
    icon_label.bind("<Button-1>", on_click)
    text_label.bind("<Button-1>", on_click)
    
    # Hover effects
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

# Create the buttons
add_btn = create_icon_button(button_frame, "Add Book", "➕", "#4CAF50", add_book)
update_btn = create_icon_button(button_frame, "Update Book", "✏️", "#2196F3", update_book)

# Back button with icon
def go_back():
    root.destroy()
    import home_page
    home_page.root.mainloop()

back_frame = Frame(container, bg="#a6093d", relief="raised", bd=2)
back_frame.place(x=20, y=20)

back_icon = Label(back_frame, text="←", font=("Arial", 16), 
                  bg="#a6093d", fg="white")
back_icon.pack(side=LEFT, padx=5)

back_text = Label(back_frame, text="Back to Home", font=("Arial", 12), 
                  bg="#a6093d", fg="white")
back_text.pack(side=LEFT, padx=(0, 5))

# Bind click events to back button
def on_back_click(e):
    go_back()

back_frame.bind("<Button-1>", on_back_click)
back_icon.bind("<Button-1>", on_back_click)
back_text.bind("<Button-1>", on_back_click)

# Hover effect for back button
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