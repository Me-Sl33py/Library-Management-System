import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import bcrypt
import database_operations  # Your database functions

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.configure(bg="#0d1b4c")
        self.mode_var = tk.StringVar(value="login")  # default mode

        self.build_ui()

    def build_ui(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Top toggle for login/signup
        toggle_frame = tk.Frame(self.root, bg="#0d1b4c")
        toggle_frame.pack(pady=10)

        tk.Radiobutton(toggle_frame, text="Existing User", variable=self.mode_var, value="login",
                       bg="#0d1b4c", fg="white", command=self.build_form).pack(side="left", padx=10)
        tk.Radiobutton(toggle_frame, text="New User", variable=self.mode_var, value="signup",
                       bg="#0d1b4c", fg="white", command=self.build_form).pack(side="left", padx=10)

        # Main container
        main_frame = tk.Frame(self.root, bg="#b3003c")
        main_frame.pack(fill="both", expand=True, padx=60, pady=20)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Left side - logo and title
        left_frame = tk.Frame(main_frame, bg="#b3003c")
        left_frame.grid(row=0, column=0)

        try:
            img_left = Image.open("logo.png")
            img_left = img_left.resize((180, 180))
            logo_img = ImageTk.PhotoImage(img_left)
        except:
            logo_img = None

        logo_label = tk.Label(left_frame, image=logo_img, bg="#b3003c")
        logo_label.image = logo_img
        logo_label.pack(pady=20)

        tk.Label(left_frame,
                 text="Library\nManagement",
                 font=("Arial", 30),
                 fg="white",
                 bg="#b3003c",
                 justify="center").pack()

        # Middle line
        tk.Frame(main_frame, bg="white", width=2).grid(row=0, column=1, sticky="ns", padx=20)

        # Right side - forms
        self.right_side = tk.Frame(main_frame, bg="#b3003c")
        self.right_side.grid(row=0, column=2, padx=60)

        try:
            img_right = Image.open("profile.png")
            img_right = img_right.resize((120, 120))
            right_img = ImageTk.PhotoImage(img_right)
        except:
            right_img = None

        right_img_label = tk.Label(self.right_side, image=right_img, bg="#b3003c")
        right_img_label.image = right_img
        right_img_label.pack(pady=(20, 10))

        # Build initial form
        self.build_form()

    def build_form(self):
        # Clear previous form widgets
        for widget in self.right_side.winfo_children():
            widget.destroy()

        mode = self.mode_var.get()
        if mode == "login":
            self.build_login_form()
        else:
            self.build_signup_form()

    def switch_to_signup(self):
        self.mode_var.set("signup")
        self.build_form()

    def switch_to_login(self):
        self.mode_var.set("login")
        self.build_form()

    def build_login_form(self):
        # Email or Username
        tk.Label(self.right_side, text="Email or Username", bg="#b3003c", font=("Arial", 13)).pack(pady=(10, 5))
        self.login_user_entry = tk.Entry(self.right_side, font=("Arial", 14), bg="#e6e6e6")
        self.login_user_entry.pack(ipady=8, fill="x")

        # Password
        tk.Label(self.right_side, text="Password", bg="#b3003c", font=("Arial", 13)).pack(pady=(10, 5))
        self.login_pass_entry = tk.Entry(self.right_side, font=("Arial", 14), bg="#e6e6e6", show="*")
        self.login_pass_entry.pack(ipady=8, fill="x")

        # Show password checkbox
        self.login_show_pwd_var = tk.BooleanVar()
        tk.Checkbutton(self.right_side, text="Show Password", variable=self.login_show_pwd_var,
                       bg="#b3003c", command=self.toggle_login_password).pack(pady=5)

        # Role selection using checkboxes (square)
        role_frame = tk.Frame(self.right_side, bg="#b3003c")
        role_frame.pack(pady=10)

        self.admin_check_var = tk.BooleanVar()
        self.user_check_var = tk.BooleanVar()

        tk.Checkbutton(role_frame, text="Admin", variable=self.admin_check_var, bg="#b3003c", indicatoron=True).pack(side="left", padx=10)
        tk.Checkbutton(role_frame, text="User", variable=self.user_check_var, bg="#b3003c", indicatoron=True).pack(side="left", padx=10)

        # Buttons
        btn_frame = tk.Frame(self.right_side, bg="#b3003c")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Login", width=12, bg="#f2f2f2", command=self.handle_login).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Switch to Sign Up", width=15, bg="#f2f2f2", command=self.switch_to_signup).pack(side="left", padx=10)

    def toggle_login_password(self):
        if self.login_show_pwd_var.get():
            self.login_pass_entry.config(show="")
        else:
            self.login_pass_entry.config(show="*")

    def build_signup_form(self):
        # Email
        tk.Label(self.right_side, text="Email", bg="#b3003c", font=("Arial", 13)).pack(pady=(10, 5))
        self.signup_email_entry = tk.Entry(self.right_side, font=("Arial", 14), bg="#e6e6e6")
        self.signup_email_entry.pack(ipady=8, fill="x")

        # Username
        tk.Label(self.right_side, text="Username", bg="#b3003c", font=("Arial", 13)).pack(pady=(10, 5))
        self.signup_username_entry = tk.Entry(self.right_side, font=("Arial", 14), bg="#e6e6e6")
        self.signup_username_entry.pack(ipady=8, fill="x")

        # Password
        tk.Label(self.right_side, text="Password", bg="#b3003c", font=("Arial", 13)).pack(pady=(10, 5))
        self.signup_pass_entry = tk.Entry(self.right_side, font=("Arial", 14), bg="#e6e6e6", show="*")
        self.signup_pass_entry.pack(ipady=8, fill="x")

        # Confirm Password
        tk.Label(self.right_side, text="Confirm Password", bg="#b3003c", font=("Arial", 13)).pack(pady=(10, 5))
        self.signup_confirm_entry = tk.Entry(self.right_side, font=("Arial", 14), bg="#e6e6e6", show="*")
        self.signup_confirm_entry.pack(ipady=8, fill="x")

        # Show password checkbox
        self.signup_show_pwd_var = tk.BooleanVar()
        tk.Checkbutton(self.right_side, text="Show Passwords", variable=self.signup_show_pwd_var,
                       bg="#b3003c", command=self.toggle_signup_passwords).pack(pady=5)

        # Role selection with radiobuttons
        role_frame = tk.Frame(self.right_side, bg="#b3003c")
        role_frame.pack(pady=10)

        self.signup_role_var = tk.StringVar(value="User")
        tk.Radiobutton(role_frame, text="Admin", variable=self.signup_role_var, value="Admin", bg="#b3003c").pack(side="left", padx=10)
        tk.Radiobutton(role_frame, text="User", variable=self.signup_role_var, value="User", bg="#b3003c").pack(side="left", padx=10)

        # Buttons
        btn_frame = tk.Frame(self.right_side, bg="#b3003c")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Sign Up", width=12, bg="#f2f2f2", command=self.handle_signup).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Switch to Login", width=15, bg="#f2f2f2", command=self.switch_to_login).pack(side="left", padx=10)

    def toggle_signup_passwords(self):
        show = "" if self.signup_show_pwd_var.get() else "*"
        self.signup_pass_entry.config(show=show)
        self.signup_confirm_entry.config(show=show)

    def handle_login(self):
        user_input = self.login_user_entry.get().strip()
        password = self.login_pass_entry.get().strip()

        # Determine selected role
        role_selected = None
        if self.admin_check_var.get():
            role_selected = "Admin"
        elif self.user_check_var.get():
            role_selected = "User"
        else:
            messagebox.showerror("Error", "Please select a role.")
            return

        if not user_input or not password:
            messagebox.showerror("Error", "Please enter all fields.")
            return

        # Fetch user from database
        user = database_operations.get_user_by_username(user_input)
        if user:
            stored_hash = user['password']
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                if user['role'] != role_selected:
                    messagebox.showerror("Error", "Role mismatch.")
                    return
                messagebox.showinfo("Success", f"Logged in as {role_selected}")
                self.open_homepage(role_selected)
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "User does not exist.")

    def handle_signup(self):
        email = self.signup_email_entry.get().strip()
        username = self.signup_username_entry.get().strip()
        password = self.signup_pass_entry.get().strip()
        confirm_password = self.signup_confirm_entry.get().strip()
        role = self.signup_role_var.get()

        if not email or not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        success, msg = database_operations.add_user_with_password(username, hashed_pwd, role)
        if success:
            messagebox.showinfo("Success", "Registration successful. You can now log in.")
            self.switch_to_login()
        else:
            messagebox.showerror("Error", msg)

    def open_homepage(self, role):
        if role == "Admin":
            messagebox.showinfo("Homepage", "Welcome Admin! (Implement home_page.py)")
        else:
            messagebox.showinfo("Homepage", "Welcome User! (Implement home_page_user.py)")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()