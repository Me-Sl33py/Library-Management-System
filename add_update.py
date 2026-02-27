from tkinter import *
from function_header_body import header_part, body_part, hover_color
import tkinter.messagebox as messagebox
from database_operations import add_book_to_db, update_book_in_db, get_book_by_id

root = Tk()
root.title("Library Management System - Add/Update Book")
root.geometry("1220x900")
root.iconbitmap("logo_icon.ico")

header = header_part(root)
body = body_part(root)

# Main container with scrollbar
container = Frame(body, bg="#5D48B8")
container.place(relx=0.5, rely=0.5, anchor=CENTER)

# anvas with scrollbar
canvas = Canvas(container, bg="#5D48B8", width=850, height=500)
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

# Title
title_frame = Frame(content_frame, bg="#5D48B8")
title_frame.pack(pady=30)

title_icon = Label(title_frame, text="📖", font=("Arial", 40), 
                   bg="#0d1b4c", fg="white")
title_icon.pack(side=LEFT, padx=10)

title_label = Label(title_frame, text="Add / Update Book", 
                   bg="#5D48B8", fg="white", font=("Arial", 24, "bold"))
title_label.pack(side=LEFT)

# Form frame
form_frame = Frame(content_frame, bg="#0d1b4c")
form_frame.pack(pady=20)

# Labels and Entries
def create_form_row(icon, label_text, row):
    label_frame = Frame(form_frame, bg="#0d1b4c")
    label_frame.grid(row=row, column=0, padx=20, pady=15, sticky="w")
    
    icon_label = Label(label_frame, text=icon, font=("Arial", 16), 
                       bg="#0d1b4c", fg="white")
    icon_label.pack(side=LEFT, padx=(0, 10))
    
    Label(label_frame, text=label_text, bg="#5D48B8", fg="white", 
          font=("Arial", 14)).pack(side=LEFT)
    
    entry = Entry(form_frame, font=("Arial", 14), width=40)
    entry.grid(row=row, column=1, padx=20, pady=15)
    return entry

#form
book_id_entry = create_form_row("🆔", "Book ID (for update only):", 0)
book_name_entry = create_form_row("📕", "Book Name:", 1)
author_entry = create_form_row("✍️", "Author:", 2)
year_entry = create_form_row("📅", "Published Year:", 3)
quantity_entry = create_form_row("🔢", "Quantity:", 4)


# Buttons frame
button_frame = Frame(content_frame, bg="#5D48B8")
button_frame.pack(pady=30)

def add_book():
    name = book_name_entry.get().strip()
    author = author_entry.get().strip()
    year = year_entry.get().strip()
    quantity = quantity_entry.get().strip()
    
    if not all([name, author, year, quantity]):
        messagebox.showerror("Error", "All fields except Book ID are required!")
        return
    
    try:
        year_int = int(year)
        quantity_int = int(quantity)
        
        if year_int < 0:
            messagebox.showerror("Error", "Year must be a positive number!")
            return
        
        if quantity_int <= 0:
            messagebox.showerror("Error", "Quantity must be greater than 0!")
            return
        
        if add_book_to_db(name, author, year_int, quantity_int):
            messagebox.showinfo("Success", "Book added successfully to database!")
            clear_form()
        else:
            messagebox.showerror("Error", "Failed to add book to database!")
        
    except ValueError:
        messagebox.showerror("Error", "Year and Quantity must be valid numbers!")

def update_book():
    book_id = book_id_entry.get().strip()
    name = book_name_entry.get().strip()
    author = author_entry.get().strip()
    year = year_entry.get().strip()
    quantity = quantity_entry.get().strip()
    
    if not book_id:
        messagebox.showerror("Error", "Book ID is required for update!")
        return
    
    if not all([name, author, year, quantity]):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        book_id_int = int(book_id)
        year_int = int(year)
        quantity_int = int(quantity)
        
        if year_int < 0:
            messagebox.showerror("Error", "Year must be a positive number!")
            return
        
        if quantity_int < 0:
            messagebox.showerror("Error", "Quantity must be 0 or greater!")
            return
        
        confirm = messagebox.askyesno("Confirm Update", 
                                      f"Update Book ID {book_id_int}?\n\n"
                                      f"Title: {name}\n"
                                      f"Author: {author}\n"
                                      f"Year: {year_int}\n"
                                      f"Quantity: {quantity_int}")
        
        if confirm:
            success, message = update_book_in_db(book_id_int, name, author, year_int, quantity_int)
            
            if success:
                messagebox.showinfo("Success", message)
                clear_form()
            else:
                messagebox.showerror("Error", message)
        
    except ValueError:
        messagebox.showerror("Error", "Book ID, Year and Quantity must be valid numbers!")

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

#  buttons
add_btn = create_icon_button(button_frame, "Add Book", "➕", "#4CAF50", add_book)
update_btn = create_icon_button(button_frame, "Update Book", "✏️", "#2196F3", update_book)

# Clear button
def clear_form():
    book_id_entry.delete(0, END)
    book_name_entry.delete(0, END)
    author_entry.delete(0, END)
    year_entry.delete(0, END)
    quantity_entry.delete(0, END)

clear_btn = create_icon_button(button_frame, "Clear Form", "🗑️", "#FF9800", clear_form)

# Back button
def go_back():
    root.destroy()
    import home_page
    home_page.root.mainloop()

back_frame = Frame(content_frame, bg="#a6093d", relief="raised", bd=2)
back_frame.place(x=20, y=20)

back_icon = Label(back_frame, text="←", font=("Arial", 16), 
                  bg="#a6093d", fg="white")
back_icon.pack(side=LEFT, padx=5)

back_text = Label(back_frame, text="Back to Home", font=("Arial", 12), 
                  bg="#a6093d", fg="white")
back_text.pack(side=LEFT, padx=(0, 5))

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

# Instructions
instructions_frame = Frame(content_frame, bg="#5D48B8")
instructions_frame.pack(pady=20)

instructions_text = """Instructions:
• To ADD: Leave Book ID empty, fill other fields, click 'Add Book'
• To UPDATE: Enter Book ID, fill all fields, click 'Update Book'
• To CLEAR: Click 'Clear Form'"""

instructions_label = Label(instructions_frame, text=instructions_text, 
                          bg="#5D48B8", fg="white", font=("Arial", 10), 
                          justify=LEFT)
instructions_label.pack()

# Set focus
book_name_entry.focus_set()

# Add mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

root.mainloop()