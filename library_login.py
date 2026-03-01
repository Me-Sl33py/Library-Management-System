import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import database_operations

#                                    
# SECRET KEY — only people with this can create admin accounts
# Accepted values: '2684' or 'dust'
ADMIN_SECRET_KEYS = {"2684", "dust"}
#                                    


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1220x900")
        self.root.iconbitmap("logo_icon.ico")
        self.root.configure(bg="#0d1b4c")

        self.mode_var = tk.StringVar(value="login")
        self.build_ui()

    #                                  
    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        #   Top toggle                         
        toggle_frame = tk.Frame(self.root, bg="#0d1b4c")
        toggle_frame.pack(pady=10)

        for text, value in [("Existing User", "login"), ("New User", "signup")]:
            tk.Radiobutton(
                toggle_frame, text=text,
                variable=self.mode_var, value=value,
                bg="#0d1b4c", fg="white", selectcolor="#0d1b4c",
                activebackground="#0d1b4c", activeforeground="white",
                font=("Arial", 12),
                command=self.build_form
            ).pack(side="left", padx=15)

        #   Main red container                     
        main_frame = tk.Frame(self.root, bg="#b3003c")
        main_frame.pack(fill="both", expand=True, padx=60, pady=20)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        #   Left side — logo + title                  
        left_frame = tk.Frame(main_frame, bg="#b3003c")
        left_frame.grid(row=0, column=0, sticky="nsew")

        try:
            img = Image.open("logo.png").resize((180, 180))
            logo_img = ImageTk.PhotoImage(img)
            lbl = tk.Label(left_frame, image=logo_img, bg="#b3003c")
            lbl.image = logo_img
            lbl.pack(pady=(60, 20))
        except Exception:
            tk.Label(left_frame, text="📚", font=("Arial", 80),
                     bg="#b3003c").pack(pady=(60, 20))

        tk.Label(
            left_frame,
            text="Library\nManagement\nSystem",
            font=("Arial", 28, "bold"),
            fg="white", bg="#b3003c",
            justify="center"
        ).pack()

        #   Demo accounts hint                     
        # demo_text = (
        #     "  Demo Accounts  \n"
        #     "Admin:  Manish / adminpass\n"
        #     "Admin:  Tshering / adminpass\n"
        #     "User:   Hilson / userpass1\n"
        #     "User:   Bibek / userpass2"
        # )
        # tk.Label(
        #     left_frame,
        #     text=demo_text,
        #     font=("Courier", 10),
        #     fg="#ffcccc", bg="#b3003c",
        #     justify="left"
        # ).pack(pady=(30, 0))

        #   Divider                           
        tk.Frame(main_frame, bg="white", width=2).grid(
            row=0, column=1, sticky="ns", padx=20)

        #   Right side — form                      
        self.right_side = tk.Frame(main_frame, bg="#b3003c")
        self.right_side.grid(row=0, column=2, sticky="nsew", padx=60)

        try:
            img2 = Image.open("profile.png").resize((100, 100))
            profile_img = ImageTk.PhotoImage(img2)
            pl = tk.Label(self.right_side, image=profile_img, bg="#b3003c")
            pl.image = profile_img
            pl.pack(pady=(40, 10))
        except Exception:
            tk.Label(self.right_side, text="👤", font=("Arial", 60),
                     bg="#b3003c").pack(pady=(40, 10))

        self.build_form()

    #                                  
    def build_form(self):
        """Clear old form widgets (keep profile image) and rebuild."""
        children = self.right_side.winfo_children()
        for widget in children[1:]:
            widget.destroy()

        if self.mode_var.get() == "login":
            self.build_login_form()
        else:
            self.build_signup_form()

    #                                  
    def build_login_form(self):
        rs = self.right_side

        tk.Label(rs, text="Username", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.login_user_entry = tk.Entry(rs, font=("Arial", 13), bg="#e6e6e6", width=28)
        self.login_user_entry.pack(ipady=6)

        tk.Label(rs, text="Password", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.login_pass_entry = tk.Entry(rs, font=("Arial", 13), bg="#e6e6e6",
                                         show="*", width=28)
        self.login_pass_entry.pack(ipady=6)

        self.login_show_var = tk.BooleanVar()
        tk.Checkbutton(
            rs, text="Show Password",
            variable=self.login_show_var,
            bg="#b3003c", fg="white", selectcolor="#b3003c",
            activebackground="#b3003c",
            command=lambda: self.login_pass_entry.config(
                show="" if self.login_show_var.get() else "*")
        ).pack(pady=5)

        tk.Label(rs, text="Login as:", bg="#b3003c", fg="white",
                 font=("Arial", 12)).pack(pady=(10, 3))
        self.login_role_var = tk.StringVar(value="user")
        role_frame = tk.Frame(rs, bg="#b3003c")
        role_frame.pack()
        for text, value in [("Admin", "admin"), ("User", "user")]:
            tk.Radiobutton(
                role_frame, text=text,
                variable=self.login_role_var, value=value,
                bg="#b3003c", fg="white", selectcolor="#b3003c",
                activebackground="#b3003c",
                font=("Arial", 12)
            ).pack(side="left", padx=15)

        btn_frame = tk.Frame(rs, bg="#b3003c")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Login", width=12, font=("Arial", 12),
                  bg="#f2f2f2", command=self.handle_login).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Sign Up Instead", width=15, font=("Arial", 12),
                  bg="#f2f2f2",
                  command=lambda: [self.mode_var.set("signup"),
                                   self.build_form()]).pack(side="left", padx=8)

        self.root.bind("<Return>", lambda e: self.handle_login())
        self.login_user_entry.focus_set()

    #                                  
    def build_signup_form(self):
        rs = self.right_side

        tk.Label(rs, text="Username", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.signup_username_entry = tk.Entry(rs, font=("Arial", 13), bg="#e6e6e6", width=28)
        self.signup_username_entry.pack(ipady=6)

        tk.Label(rs, text="Password  (min 8 characters)", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.signup_pass_entry = tk.Entry(rs, font=("Arial", 13), bg="#e6e6e6",
                                          show="*", width=28)
        self.signup_pass_entry.pack(ipady=6)

        tk.Label(rs, text="Confirm Password", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.signup_confirm_entry = tk.Entry(rs, font=("Arial", 13), bg="#e6e6e6",
                                             show="*", width=28)
        self.signup_confirm_entry.pack(ipady=6)

        self.signup_show_var = tk.BooleanVar()
        def toggle_signup_passwords():
            show = "" if self.signup_show_var.get() else "*"
            self.signup_pass_entry.config(show=show)
            self.signup_confirm_entry.config(show=show)

        tk.Checkbutton(
            rs, text="Show Passwords",
            variable=self.signup_show_var,
            bg="#b3003c", fg="white", selectcolor="#b3003c",
            activebackground="#b3003c",
            command=toggle_signup_passwords
        ).pack(pady=5)

        tk.Label(rs, text="Register as:", bg="#b3003c", fg="white",
                 font=("Arial", 12)).pack(pady=(5, 3))
        self.signup_role_var = tk.StringVar(value="user")
        role_frame = tk.Frame(rs, bg="#b3003c")
        role_frame.pack()
        for text, value in [("Admin", "admin"), ("User", "user")]:
            tk.Radiobutton(
                role_frame, text=text,
                variable=self.signup_role_var, value=value,
                bg="#b3003c", fg="white", selectcolor="#b3003c",
                activebackground="#b3003c",
                font=("Arial", 12),
                command=self.toggle_admin_key_field
            ).pack(side="left", padx=15)

        #   Admin secret key field (hidden until Admin is selected)   
        self.admin_key_frame = tk.Frame(rs, bg="#b3003c")
        tk.Label(self.admin_key_frame,
                 text="🔑  Admin Secret Key",
                 bg="#b3003c", fg="#ffcccc",
                 font=("Arial", 12, "bold")).pack(pady=(8, 3))
        self.admin_key_entry = tk.Entry(self.admin_key_frame, font=("Arial", 13),
                                        bg="#e6e6e6", show="*", width=28)
        self.admin_key_entry.pack(ipady=6)
        tk.Label(self.admin_key_frame,
                 text="Don't have the key? Contact your administrator.",
                 bg="#b3003c", fg="#ffaaaa",
                 font=("Arial", 9, "italic")).pack(pady=(3, 0))
        # Hidden by default
        self.admin_key_frame.pack_forget()

        # Buttons
        self.signup_btn_frame = tk.Frame(rs, bg="#b3003c")
        self.signup_btn_frame.pack(pady=15)
        tk.Button(self.signup_btn_frame, text="Sign Up", width=12, font=("Arial", 12),
                  bg="#f2f2f2", command=self.handle_signup).pack(side="left", padx=8)
        tk.Button(self.signup_btn_frame, text="Login Instead", width=15, font=("Arial", 12),
                  bg="#f2f2f2",
                  command=lambda: [self.mode_var.set("login"),
                                   self.build_form()]).pack(side="left", padx=8)

        self.root.bind("<Return>", lambda e: self.handle_signup())
        self.signup_username_entry.focus_set()

    #                                  
    def toggle_admin_key_field(self):
        """Show the secret key field only when Admin role is selected."""
        if self.signup_role_var.get() == "admin":
            # Insert key frame just before the button frame
            self.admin_key_frame.pack(pady=(5, 0), before=self.signup_btn_frame)
        else:
            self.admin_key_frame.pack_forget()

    #                                  
    def handle_login(self):
        username = self.login_user_entry.get().strip()
        password = self.login_pass_entry.get()   # no strip — spaces count
        role     = self.login_role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        if not database_operations.verify_user_credentials(username, password):
            messagebox.showerror("Error", "Incorrect username or password.")
            return

        user = database_operations.get_user_by_username(username)
        if not user:
            messagebox.showerror("Error", "User not found.")
            return

        if user['role'] != role:
            messagebox.showerror(
                "Role Mismatch",
                f"This account is registered as '{user['role']}', not '{role}'.\n"
                "Please select the correct role."
            )
            return

        messagebox.showinfo("Welcome", f"Welcome, {username}! 👋")
        self.open_homepage(role, username)

    #                                  
    def handle_signup(self):
        username         = self.signup_username_entry.get().strip()
        password         = self.signup_pass_entry.get()       # no strip — spaces count
        confirm_password = self.signup_confirm_entry.get()    # no strip — spaces count
        role             = self.signup_role_var.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        # ✅ Min 8 characters, spaces count
        if len(password) < 8:
            messagebox.showerror(
                "Weak Password",
                "Password must be at least 8 characters long.\n"
                "(Spaces count as characters too!)"
            )
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # ✅ Admin secret key gate
        if role == "admin":
            entered_key = self.admin_key_entry.get().strip()
            if entered_key not in ADMIN_SECRET_KEYS:
                messagebox.showerror(
                    "Access Denied 🔒",
                    "Invalid admin secret key.\n\n"
                    "You need the correct key to create an admin account.\n"
                    "Please contact your administrator."
                )
                return

        success, msg = database_operations.add_user_with_password(username, password, role)
        if success:
            messagebox.showinfo(
                "Account Created! ✅",
                f"Welcome, {username}!\n"
                f"Account created as '{role}'.\n"
                "You can now log in."
            )
            self.mode_var.set("login")
            self.build_form()
        else:
            messagebox.showerror("Error", msg)

    #                                  
    def open_homepage(self, role, username):
        import importlib
        if role == "admin":
            self.root.destroy()
            # ✅ Pass username so it flows through every page
            importlib.import_module("home_page").run(username)
        else:
            messagebox.showinfo(
                "🚧 Under Construction",
                "The User portal is still under construction.\n"
                "Please check back soon!"
            )


#                                    
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()