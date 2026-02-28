from tkinter import *
from function_header_body import header_part, body_part
import tkinter.messagebox as messagebox
from database_operations import get_all_users, delete_user_from_db

root = Tk()
root.title("Library Management System - Manage Users")
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

# Update scrollregion
def update_scrollregion(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", update_scrollregion)

# Back button at top left 
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

title_icon = Label(title_frame, text="👥", font=("Arial", 40), 
                   bg="#5D48B8", fg="white")
title_icon.pack(side=LEFT, padx=10)

title_label = Label(title_frame, text="Registered Users", 
                   bg="#5D48B8", fg="white", font=("Arial", 24, "bold"))
title_label.pack(side=LEFT)

# Table frame
table_frame = Frame(content_frame, bg="#0d1b4c")
table_frame.pack(pady=20, padx=20)

# Create table headers
headers = ["User ID", "Username", "Role", "Delete"]
for i, header in enumerate(headers):
    Label(table_frame, text=header, bg="#0d1b4c", fg="white", 
          font=("Arial", 12, "bold"), width=20, relief="ridge").grid(row=0, column=i, padx=2, pady=2)

# icon button
def create_icon_button(parent, text, icon, color, command, row, col):
    btn_frame = Frame(parent, bg="white", relief="raised", bd=2)
    btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    icon_label = Label(btn_frame, text=icon, font=("Arial", 14), 
                       bg="white", fg=color)
    icon_label.pack(side=LEFT, padx=5)
    
    text_label = Label(btn_frame, text=text, font=("Arial", 12), 
                       bg="white", fg="black")
    text_label.pack(side=LEFT, padx=(0, 5))
    
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

# load and display users
def load_users():
    # Clear existing rows except headers
    for widget in table_frame.grid_slaves():
        if int(widget.grid_info()["row"]) > 0:
            widget.destroy()
    
    users = get_all_users()
    if not users:
        Label(table_frame, text="No users found", bg="#0d1b4c", fg="white", 
              font=("Arial", 12), width=80).grid(row=1, column=0, columnspan=4, pady=10)
        return
        
    for idx, user in enumerate(users, start=1):
        row_color = "#1a237e" if idx % 2 == 0 else "#283593"
        
        # User ID
        Label(table_frame, text=user['user_id'], bg=row_color, fg="white", 
              font=("Arial", 11), width=20, relief="ridge").grid(row=idx, column=0, padx=2, pady=2)
        
        # Username
        Label(table_frame, text=user['username'], bg=row_color, fg="white", 
              font=("Arial", 11), width=20, relief="ridge").grid(row=idx, column=1, padx=2, pady=2)
        
        # Role with color coding
        role_text = user['role']
        role_color = "#FF6347" if role_text == "admin" else "#32CD32"  # Red for admin, Green for user
        Label(table_frame, text=role_text.title(), bg=row_color, fg=role_color, 
              font=("Arial", 11, "bold"), width=20, relief="ridge").grid(row=idx, column=2, padx=2, pady=2)
        
        # Delete button for non-admin users only
        if user['role'] != 'admin':
            def delete_user(user_id=user['user_id'], username=user['username']):
                # Show confirmation dialog
                confirm = messagebox.askyesno("Confirm Delete", 
                    f"Are you sure you want to delete user:\n\n"
                    f"Username: {username}\n"
                    f"User ID: {user_id}\n\n"
                    "This action cannot be undone!")
                
                if confirm:
                    success, message = delete_user_from_db(user_id)
                    if success:
                        messagebox.showinfo("Success", message)
                        load_users()  # Refresh the list
                    else:
                        messagebox.showerror("Error", message)
            
            create_icon_button(table_frame, "Delete", "🗑️", "#F44336", delete_user, idx, 3)
        else:
            # Show message for admin users
            admin_label = Label(table_frame, text="Cannot Delete Admin", bg=row_color, fg="#FF6347", 
                                font=("Arial", 10, "italic"), width=20, relief="ridge")
            admin_label.grid(row=idx, column=3, padx=2, pady=2)
            
            
            def on_admin_enter(e, label=admin_label, bg=row_color):
                label.config(bg="#FFCCCB", fg="#E04141")
            
            def on_admin_leave(e, label=admin_label, bg=row_color, fg="#FF6347"):
                label.config(bg=bg, fg=fg)
            
            admin_label.bind("<Enter>", on_admin_enter)
            admin_label.bind("<Leave>", on_admin_leave)

# Load users 
load_users()

# Refresh button 
def create_top_icon_button(parent, text, icon, color, command):
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

refresh_btn = create_top_icon_button(button_frame, "Refresh List", "🔄", "#4CAF50", load_users)

# Instructions
instructions_frame = Frame(content_frame, bg="#5D48B8")
instructions_frame.pack(pady=20)

instructions_text = """Instructions:
1. View all registered users in the table above
2. Regular users can be deleted by clicking the 'Delete' button
3. Admin accounts cannot be deleted (for security reasons)
4. Click 'Refresh List' to update the user list
5. Role colors: Red = Admin, Green = User"""

instructions_label = Label(instructions_frame, text=instructions_text, 
                          bg="#5D48B8", fg="white", font=("Arial", 10), 
                          justify=LEFT)
instructions_label.pack()

# Add mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

root.mainloop()