import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk

def show_password():
    if show_pass_var.get():
        password_entry.config(show="")
        confirm_entry.config(show="")
    else:
        password_entry.config(show="*")
        confirm_entry.config(show="*")

def login():
    messagebox.showinfo("Login", "Login Clicked")

def signup():
    messagebox.showinfo("Sign Up", "Sign Up Clicked")

root = tk.Tk()
root.title("Library Management System")

root.configure(bg="#1f2a44")

main_frame = tk.Frame(root, bg="#b3003c")
main_frame.pack(fill="both", expand=True, padx=60, pady=40)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=0)
main_frame.grid_columnconfigure(2, weight=1)
main_frame.grid_rowconfigure(0, weight=1)


left_frame = tk.Frame(main_frame, bg="#b3003c")
left_frame.grid(row=0, column=0)


img_left = Image.open("logo.png")
img_left = img_left.resize((180, 180))   
logo_img = ImageTk.PhotoImage(img_left)

logo_label = tk.Label(left_frame, image=logo_img, bg="#b3003c")
logo_label.pack(pady=60)

tk.Label(left_frame,
text="Library\nManagement",
font=("Arial", 30),
fg="white",
bg="#b3003c",
justify="center").pack()


linemiddle = tk.Frame(main_frame, bg="white", width=2)
linemiddle.grid(row=0, column=1, sticky="ns", padx=20)


right_side = tk.Frame(main_frame, bg="#b3003c")
right_side.grid(row=0, column=2, padx=60)


img_right = Image.open("profile.png")
img_right = img_right.resize((120, 120))   
right_img = ImageTk.PhotoImage(img_right)

right_img_label = tk.Label(right_side, image=right_img, bg="#b3003c")
right_img_label.pack(pady=(40,20))


tk.Label(right_side, text="Username",
bg="#b3003c", font=("Arial", 13)).pack(pady=(10,5))

username_entry = tk.Entry(right_side,
font=("Arial", 14),
bg="#e6e6e6",
)
username_entry.pack(ipady=8, fill="x")


tk.Label(right_side, text="Password",
bg="#b3003c", font=("Arial", 13)).pack(pady=(20,5))

password_entry = tk.Entry(right_side,
font=("Arial", 14),
bg="#e6e6e6",
show="*")
password_entry.pack(ipady=8, fill="x")


tk.Label(right_side, text="Confirm Password",
bg="#b3003c", font=("Arial", 13)).pack(pady=(20,5))

confirm_entry = tk.Entry(right_side,
font=("Arial", 14),
bg="#e6e6e6",
show="*")
confirm_entry.pack(ipady=8, fill="x")


show_pass_var = tk.BooleanVar()
tk.Checkbutton(right_side,
text="Show password",
variable=show_pass_var,
command=show_password,
bg="#b3003c").pack(pady=10)

tk.Label(right_side, text="Role",
bg="#b3003c", font=("Arial", 12)).pack()

role_var = tk.StringVar()

role_frame = tk.Frame(right_side, bg="#b3003c")
role_frame.pack()

tk.Radiobutton(role_frame,
text="Admin",
variable=role_var,
value="Admin",
bg="#b3003c").pack(side="left", padx=10)

tk.Radiobutton(role_frame,
text="User",
variable=role_var,
value="User",
bg="#b3003c").pack(side="left", padx=10)


button_frame = tk.Frame(right_side, bg="#b3003c")
button_frame.pack(pady=40)

tk.Button(button_frame,
text="Login",
width=12,
bg="#f2f2f2",
command=login).pack(side="left", padx=20)

tk.Button(button_frame,
text="Sign up",
width=12,
bg="#f2f2f2",
command=signup).pack(side="left", padx=20)

root.mainloop()