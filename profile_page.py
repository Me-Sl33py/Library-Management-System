from tkinter import *
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part
import database_operations


def open_page(root, module_name, username=None):
    """Navigate to another page, optionally passing username."""
    root.destroy()
    import importlib
    mod = importlib.import_module(module_name)
    if username:
        mod.run(username)
    else:
        mod.run()


def run(username="Guest"):
    root = Tk()
    root.title("Library Management System - Profile")
    root.geometry("1220x900")
    root.iconbitmap("logo_icon.ico")

    #  Profile button goes back to home 
    def go_home():
        open_page(root, "home_page", username)

    header = header_part(root, username=username, on_profile_click=go_home)
    body   = body_part(root)

    #   Centered card  
    card = Frame(body, bg="#5D48B8", bd=2, relief="ridge")
    card.place(relx=0.5, rely=0.5, anchor=CENTER, width=500)

    #   Title      
    Label(card, text="👤  My Profile", font=("Arial", 22, "bold"),
          bg="#5D48B8", fg="white").pack(pady=(30, 5))

    Label(card, text=f"Logged in as:  {username}",
          font=("Arial", 13), bg="#5D48B8", fg="#d0c8ff").pack(pady=(0, 20))

    #   Divider     
    Frame(card, bg="white", height=1).pack(fill=X, padx=30)

    #   Helper to build a labeled entry                ─
    def make_field(parent, label_text, show=None):
        Label(parent, text=label_text, bg="#5D48B8", fg="white",
              font=("Arial", 12), anchor="w").pack(fill=X, padx=40, pady=(12, 2))
        entry = Entry(parent, font=("Arial", 13), bg="#e6e6e6",
                      show=show, width=35)
        entry.pack(ipady=6, padx=40, fill=X)
        return entry

    #  
    # SECTION 1 — Change Username
    #  
    Label(card, text="Change Username", font=("Arial", 14, "bold"),
          bg="#5D48B8", fg="#a8d8ff").pack(anchor="w", padx=40, pady=(20, 0))

    new_username_entry  = make_field(card, "New Username")
    cu_password_entry   = make_field(card, "Current Password (required)", show="*")

    def change_username():
        new_name    = new_username_entry.get().strip()
        cur_pass    = cu_password_entry.get()           # spaces count

        if not new_name or not cur_pass:
            messagebox.showerror("Error", "Please fill in all fields.", parent=root)
            return
        if new_name == username:
            messagebox.showerror("Error", "New username is the same as current.", parent=root)
            return

        # Verify current password
        if not database_operations.verify_user_credentials(username, cur_pass):
            messagebox.showerror("Error", "Incorrect current password.", parent=root)
            return

        # Check new username not already taken
        existing = database_operations.get_user_by_username(new_name)
        if existing:
            messagebox.showerror("Error", f"Username '{new_name}' is already taken.", parent=root)
            return

        success, msg = database_operations.update_username(username, new_name)
        if success:
            messagebox.showinfo("Success ✅",
                f"Username changed to '{new_name}'.\nPlease log in again.", parent=root)
            # Send back to login after username change
            open_page(root, "library_login")
        else:
            messagebox.showerror("Error", msg, parent=root)

    Button(card, text="✏️  Update Username", font=("Arial", 12, "bold"),
           bg="#2196F3", fg="white", padx=20, pady=8,
           cursor="hand2", command=change_username).pack(pady=(10, 5))

    #   Divider     
    Frame(card, bg="white", height=1).pack(fill=X, padx=30, pady=(15, 0))
  
    # SECTION 2 
    Label(card, text="Change Password", font=("Arial", 14, "bold"),
          bg="#5D48B8", fg="#a8d8ff").pack(anchor="w", padx=40, pady=(20, 0))

    cur_pass_entry  = make_field(card, "Current Password", show="*")
    new_pass_entry  = make_field(card, "New Password  (min 8 characters)", show="*")
    conf_pass_entry = make_field(card, "Confirm New Password", show="*")

    # Show/hide passwords toggle
    show_var = BooleanVar()
    def toggle_show():
        show = "" if show_var.get() else "*"
        for e in (cur_pass_entry, new_pass_entry, conf_pass_entry,
                  cu_password_entry):
            e.config(show=show)

    Checkbutton(card, text="Show Passwords", variable=show_var,
                bg="#5D48B8", fg="white", selectcolor="#5D48B8",
                activebackground="#5D48B8", font=("Arial", 11),
                command=toggle_show).pack(anchor="w", padx=40, pady=(6, 0))

    def change_password():
        cur_pass  = cur_pass_entry.get()          # spaces count
        new_pass  = new_pass_entry.get()          # spaces count
        conf_pass = conf_pass_entry.get()         # spaces count

        if not cur_pass or not new_pass or not conf_pass:
            messagebox.showerror("Error", "Please fill in all password fields.", parent=root)
            return

        # Verify current password
        if not database_operations.verify_user_credentials(username, cur_pass):
            messagebox.showerror("Error", "Incorrect current password.", parent=root)
            return

        if len(new_pass) < 8:
            messagebox.showerror("Error",
                "New password must be at least 8 characters.\n"
                "(Spaces count as characters too!)", parent=root)
            return

        if new_pass == cur_pass:
            messagebox.showerror("Error",
                "New password must be different from current password.", parent=root)
            return

        if new_pass != conf_pass:
            messagebox.showerror("Error", "New passwords do not match.", parent=root)
            return

        success, msg = database_operations.update_password(username, new_pass)
        if success:
            messagebox.showinfo("Success ✅",
                "Password changed successfully!\nPlease log in again.", parent=root)
            open_page(root, "library_login")
        else:
            messagebox.showerror("Error", msg, parent=root)

    Button(card, text="🔒  Update Password", font=("Arial", 12, "bold"),
           bg="#4CAF50", fg="white", padx=20, pady=8,
           cursor="hand2", command=change_password).pack(pady=(10, 5))

    #   Divider     
    Frame(card, bg="white", height=1).pack(fill=X, padx=30, pady=(15, 0))

     
    # Sign Out
     
    def sign_out():
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?",
                               parent=root):
            open_page(root, "library_login")

    Button(card, text="🚪  Sign Out", font=("Arial", 13, "bold"),
           bg="#a6093d", fg="white", padx=20, pady=10,
           cursor="hand2", command=sign_out).pack(pady=(15, 30))

    root.mainloop()


if __name__ == "__main__":
    run("Manish")   