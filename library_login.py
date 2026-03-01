import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import database_operations

ADMIN_SECRET_KEYS = {"2684", "dust"}


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1220x900")
        self.root.iconbitmap("logo_icon.ico")
        self.root.configure(bg="#0d1b4c")
        self.mode_var = tk.StringVar(value="login")
        self.build_ui()

    #  BUILD FULL UI 
    def build_ui(self):
        for w in self.root.winfo_children():
            w.destroy()

        #  Toggle row 
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

        #  Scrollable body 
        scroll_host = tk.Frame(self.root, bg="#b3003c")
        scroll_host.pack(fill="both", expand=True, padx=60, pady=(0, 20))

        canvas = tk.Canvas(scroll_host, bg="#b3003c", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        vsb = tk.Scrollbar(scroll_host, orient="vertical", command=canvas.yview)
        vsb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vsb.set)

        # content frame — full width of canvas
        self.cf = tk.Frame(canvas, bg="#b3003c")
        self._cw = canvas.create_window((0, 0), window=self.cf, anchor="nw")

        def _on_cf_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def _on_canvas_configure(e):
            canvas.itemconfig(self._cw, width=e.width)

        self.cf.bind("<Configure>", _on_cf_configure)
        canvas.bind("<Configure>", _on_canvas_configure)


        #  Inner centred layout 
        inner = tk.Frame(self.cf, bg="#b3003c")
        inner.pack(expand=True, pady=30)

        inner.grid_columnconfigure(0, weight=1)
        inner.grid_columnconfigure(1, weight=0)
        inner.grid_columnconfigure(2, weight=1)

        #  Left: logo + title 
        left = tk.Frame(inner, bg="#b3003c")
        left.grid(row=0, column=0, padx=60, sticky="n", pady=20)

        try:
            img = Image.open("logo.png").resize((180, 180))
            logo_img = ImageTk.PhotoImage(img)
            lbl = tk.Label(left, image=logo_img, bg="#b3003c")
            lbl.image = logo_img
            lbl.pack(pady=(30, 20))
        except Exception:
            tk.Label(left, text="📚", font=("Arial", 80),
                     bg="#b3003c", fg="white").pack(pady=(30, 20))

        tk.Label(
            left,
            text="Library\nManagement\nSystem",
            font=("Arial", 28, "bold"),
            fg="white", bg="#b3003c", justify="center"
        ).pack()

        #  Divider 
        tk.Frame(inner, bg="white", width=2).grid(
            row=0, column=1, sticky="ns", padx=10, pady=20)

        #  Right: profile image + form 
        self.right_side = tk.Frame(inner, bg="#b3003c")
        self.right_side.grid(row=0, column=2, padx=60, sticky="n", pady=20)

        try:
            img2 = Image.open("profile.png").resize((100, 100))
            profile_img = ImageTk.PhotoImage(img2)
            pl = tk.Label(self.right_side, image=profile_img, bg="#b3003c")
            pl.image = profile_img
            pl.pack(pady=(30, 10))
        except Exception:
            tk.Label(self.right_side, text="👤", font=("Arial", 60),
                     bg="#b3003c", fg="white").pack(pady=(30, 10))

        self.build_form()

    #  REBUILD FORM ONLY 
    def build_form(self):
        """Clear form widgets (keep profile image at index 0) and rebuild."""
        children = self.right_side.winfo_children()
        for w in children[1:]:
            w.destroy()
        if self.mode_var.get() == "login":
            self.build_login_form()
        else:
            self.build_signup_form()

    #  LOGIN FORM 
    def build_login_form(self):
        rs = self.right_side

        tk.Label(rs, text="Username", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.login_user_entry = tk.Entry(rs, font=("Arial", 13),
                                         bg="#e6e6e6", width=28)
        self.login_user_entry.pack(ipady=6)

        tk.Label(rs, text="Password", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.login_pass_entry = tk.Entry(rs, font=("Arial", 13),
                                          bg="#e6e6e6", show="*", width=28)
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
                activebackground="#b3003c", font=("Arial", 12)
            ).pack(side="left", padx=15)

        btn_frame = tk.Frame(rs, bg="#b3003c")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Login", width=12, font=("Arial", 12),
                  bg="#f2f2f2", cursor="hand2",
                  command=self.handle_login).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Sign Up Instead", width=15, font=("Arial", 12),
                  bg="#f2f2f2", cursor="hand2",
                  command=lambda: [self.mode_var.set("signup"),
                                   self.build_form()]).pack(side="left", padx=8)

        self.root.bind("<Return>", lambda e: self.handle_login())
        self.login_user_entry.focus_set()

    #  SIGNUP FORM 
    def build_signup_form(self):
        rs = self.right_side

        tk.Label(rs, text="Username", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.signup_username_entry = tk.Entry(rs, font=("Arial", 13),
                                              bg="#e6e6e6", width=28)
        self.signup_username_entry.pack(ipady=6)

        tk.Label(rs, text="Password  (min 8 characters)", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.signup_pass_entry = tk.Entry(rs, font=("Arial", 13),
                                          bg="#e6e6e6", show="*", width=28)
        self.signup_pass_entry.pack(ipady=6)

        tk.Label(rs, text="Confirm Password", bg="#b3003c", fg="white",
                 font=("Arial", 13)).pack(pady=(10, 3))
        self.signup_confirm_entry = tk.Entry(rs, font=("Arial", 13),
                                             bg="#e6e6e6", show="*", width=28)
        self.signup_confirm_entry.pack(ipady=6)

        self.signup_show_var = tk.BooleanVar()
        def toggle_signup():
            s = "" if self.signup_show_var.get() else "*"
            self.signup_pass_entry.config(show=s)
            self.signup_confirm_entry.config(show=s)
        tk.Checkbutton(
            rs, text="Show Passwords",
            variable=self.signup_show_var,
            bg="#b3003c", fg="white", selectcolor="#b3003c",
            activebackground="#b3003c",
            command=toggle_signup
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
                activebackground="#b3003c", font=("Arial", 12),
                command=self.toggle_admin_key_field
            ).pack(side="left", padx=15)

        # Admin secret key (hidden until Admin selected)
        self.admin_key_frame = tk.Frame(rs, bg="#b3003c")
        tk.Label(self.admin_key_frame, text="🔑  Admin Secret Key",
                 bg="#b3003c", fg="#ffcccc",
                 font=("Arial", 12, "bold")).pack(pady=(8, 3))
        self.admin_key_entry = tk.Entry(self.admin_key_frame, font=("Arial", 13),
                                        bg="#e6e6e6", show="*", width=28)
        self.admin_key_entry.pack(ipady=6)
        tk.Label(self.admin_key_frame,
                 text="Don't have the key? Contact your administrator.",
                 bg="#b3003c", fg="#ffaaaa",
                 font=("Arial", 9, "italic")).pack(pady=(3, 0))
        self.admin_key_frame.pack_forget()   # hidden by default

        # Buttons
        self.signup_btn_frame = tk.Frame(rs, bg="#b3003c")
        self.signup_btn_frame.pack(pady=15)
        tk.Button(self.signup_btn_frame, text="Sign Up", width=12, font=("Arial", 12),
                  bg="#f2f2f2", cursor="hand2",
                  command=self.handle_signup).pack(side="left", padx=8)
        tk.Button(self.signup_btn_frame, text="Login Instead", width=15, font=("Arial", 12),
                  bg="#f2f2f2", cursor="hand2",
                  command=lambda: [self.mode_var.set("login"),
                                   self.build_form()]).pack(side="left", padx=8)

        self.root.bind("<Return>", lambda e: self.handle_signup())
        self.signup_username_entry.focus_set()

    #  ADMIN KEY TOGGLE 
    def toggle_admin_key_field(self):
        if self.signup_role_var.get() == "admin":
            self.admin_key_frame.pack(pady=(5, 0), before=self.signup_btn_frame)
        else:
            self.admin_key_frame.pack_forget()

    #  HANDLE LOGIN 
    def handle_login(self):
        username = self.login_user_entry.get().strip()
        password = self.login_pass_entry.get()
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
            messagebox.showerror("Role Mismatch",
                f"This account is registered as '{user['role']}', not '{role}'.\n"
                "Please select the correct role.")
            return

        self.open_homepage(role, username)

    #  HANDLE SIGNUP 
    def handle_signup(self):
        username         = self.signup_username_entry.get().strip()
        password         = self.signup_pass_entry.get()
        confirm_password = self.signup_confirm_entry.get()
        role             = self.signup_role_var.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty."); return
        if len(password) < 8:
            messagebox.showerror("Weak Password",
                "Password must be at least 8 characters.\n(Spaces count too!)"); return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match."); return
        if role == "admin":
            key = self.admin_key_entry.get().strip()
            if key not in ADMIN_SECRET_KEYS:
                messagebox.showerror("Access Denied 🔒",
                    "Invalid admin secret key.\nContact your administrator."); return

        ok, msg = database_operations.add_user_with_password(username, password, role)
        if ok:
            messagebox.showinfo("Account Created! ✅",
                f"Welcome, {username}!\nAccount created as '{role}'.\nYou can now log in.")
            self.mode_var.set("login")
            self.build_form()
        else:
            messagebox.showerror("Error", msg)

    #  OPEN HOMEPAGE 
    def open_homepage(self, role, username):
        self.root.destroy()
        if role == "admin":
            import admin_main
            admin_main.AdminMain(username).mainloop()
        else:
            import user_main
            user_main.UserMain(username).mainloop()


#  ENTRY POINT 
def run():
    root = tk.Tk()
    LibraryApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()