import tkinter as tk

root = tk.Tk()
root.title("User Home Page")
root.geometry("900x700")
root.configure(bg="white")

header = tk.Frame(root, bg="#b3003c", height=80)
header.pack(fill="x")

tk.Label(header, text="Library Management System",
         bg="#b3003c", fg="white",
         font=("Arial", 20)).pack(side="left", padx=20)

tk.Label(header, text="Profile: Username",
         bg="#b3003c", fg="white",
         font=("Arial", 14)).pack(side="right", padx=20)


tk.Label(root, text="Welcome, Username!",
         font=("Arial", 18),
         bg="white").pack(pady=20)


book_frame = tk.Frame(root, bg="white")
book_frame.pack(pady=10)


tk.Label(book_frame, text="Available Books",
         font=("Arial", 14, "bold"),
         bg="white").grid(row=0, column=0, padx=100)


tk.Label(book_frame, text="My Books",
         font=("Arial", 14, "bold"),
         bg="white").grid(row=0, column=1, padx=100)


box1 = tk.Frame(book_frame, bd=1, relief="solid", padx=20, pady=20)
box1.grid(row=1, column=0, padx=50, pady=20)

tk.Label(box1, text="Python 101").pack()
tk.Button(box1, text="Request").pack(pady=10)

box2 = tk.Frame(book_frame, bd=1, relief="solid", padx=20, pady=20)
box2.grid(row=2, column=0, padx=50, pady=20)

tk.Label(box2, text="Math 2001").pack()
tk.Button(box2, text="Request").pack(pady=10)


box3 = tk.Frame(book_frame, bd=1, relief="solid", padx=20, pady=20)
box3.grid(row=1, column=1, padx=50, pady=20)

tk.Label(box3, text="Solution 243").pack()
tk.Button(box3, text="Return").pack(pady=10)


box4 = tk.Frame(book_frame, bd=1, relief="solid", padx=20, pady=20)
box4.grid(row=2, column=1, padx=50, pady=20)

tk.Label(box4, text="World War 2").pack()
tk.Button(box4, text="Return").pack(pady=10)

bottom = tk.Frame(root, bd=1, relief="solid", padx=20, pady=20)
bottom.pack(fill="x", pady=30, padx=40)

tk.Label(bottom, text="My Books",
         font=("Arial", 14, "bold")).pack(anchor="w")

tk.Label(bottom, text="✔ Book X (Due: 10/26)").pack(anchor="w")
tk.Label(bottom, text="✔ Book Y (Due: 8/26)").pack(anchor="w")

root.mainloop()