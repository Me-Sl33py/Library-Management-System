from tkinter import *
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part
from database_operations import get_all_users, delete_user_from_db


def open_page(root, module_name):
    root.destroy()
    import importlib
    importlib.import_module(module_name).run()


def run():
    root = Tk()
    root.title("Library Management System - Manage Users")
    root.geometry("1220x900")
    root.iconbitmap("logo_icon.ico")

    header = header_part(root)
    body   = body_part(root)

    container = Frame(body, bg="#5D48B8")
    container.place(relx=0.5, rely=0.5, anchor=CENTER)

    canvas = Canvas(container, bg="#5D48B8", width=850, height=500)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    content_frame = Frame(canvas, bg="#5D48B8")
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def update_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_frame.bind("<Configure>", update_scrollregion)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ── Back button ────────────────────────────────────────────────
    back_frame = Frame(content_frame, bg="#a6093d", relief="raised", bd=2)
    back_frame.pack(anchor="w", padx=20, pady=(15, 0))
    back_icon = Label(back_frame, text="←", font=("Arial", 16), bg="#a6093d", fg="white")
    back_icon.pack(side=LEFT, padx=5)
    back_text = Label(back_frame, text="Back to Home", font=("Arial", 12), bg="#a6093d", fg="white")
    back_text.pack(side=LEFT, padx=(0, 5))

    def on_back_click(e): open_page(root, "home_page")
    def on_back_enter(e):
        for w in (back_frame, back_icon, back_text): w.config(bg="#4fe4ee")
    def on_back_leave(e):
        for w in (back_frame, back_icon, back_text): w.config(bg="#a6093d")
    for widget in (back_frame, back_icon, back_text):
        widget.bind("<Button-1>", on_back_click)
        widget.bind("<Enter>",    on_back_enter)
        widget.bind("<Leave>",    on_back_leave)

    # ── Title ──────────────────────────────────────────────────────
    title_frame = Frame(content_frame, bg="#5D48B8")
    title_frame.pack(pady=30)
    Label(title_frame, text="👥", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
    Label(title_frame, text="Registered Users", bg="#5D48B8", fg="white",
          font=("Arial", 24, "bold")).pack(side=LEFT)

    # ── Table ──────────────────────────────────────────────────────
    table_frame = Frame(content_frame, bg="#0d1b4c")
    table_frame.pack(pady=20, padx=20)

    for i, h in enumerate(["User ID", "Username", "Role", "Delete"]):
        Label(table_frame, text=h, bg="#0d1b4c", fg="white",
              font=("Arial", 12, "bold"), width=20, relief="ridge").grid(
            row=0, column=i, padx=2, pady=2)

    # ── Single reusable icon button (grid version) ─────────────────
    # ✅ Removed the duplicate create_top_icon_button function
    def create_icon_button(parent, text, icon, color, command, row=None, col=None, use_pack=False):
        bf = Frame(parent, bg="white", relief="raised", bd=2)
        if use_pack:
            bf.pack(side=LEFT, padx=10)
        else:
            bf.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        il = Label(bf, text=icon, font=("Arial", 14 if not use_pack else 20), bg="white", fg=color)
        il.pack(side=LEFT, padx=5 if not use_pack else 10)
        tl = Label(bf, text=text, font=("Arial", 12 if not use_pack else 14, "bold"), bg="white", fg="black")
        tl.pack(side=LEFT, padx=(0, 5 if not use_pack else 10))
        def on_click(e): command()
        def on_enter(e):
            bf.config(bg="lightblue"); il.config(bg="lightblue"); tl.config(bg="lightblue")
        def on_leave(e):
            bf.config(bg="white"); il.config(bg="white"); tl.config(bg="white")
        for w in (bf, il, tl):
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)
        return bf

    def load_users():
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
            Label(table_frame, text=user['user_id'],  bg=row_color, fg="white",
                  font=("Arial", 11), width=20, relief="ridge").grid(row=idx, column=0, padx=2, pady=2)
            Label(table_frame, text=user['username'], bg=row_color, fg="white",
                  font=("Arial", 11), width=20, relief="ridge").grid(row=idx, column=1, padx=2, pady=2)
            role_color = "#FF6347" if user['role'] == "admin" else "#32CD32"
            Label(table_frame, text=user['role'].title(), bg=row_color, fg=role_color,
                  font=("Arial", 11, "bold"), width=20, relief="ridge").grid(row=idx, column=2, padx=2, pady=2)
            if user['role'] != 'admin':
                def delete_user(uid=user['user_id'], uname=user['username']):
                    if messagebox.askyesno("Confirm Delete",
                                           f"Delete user:\nUsername: {uname}\nUser ID: {uid}\n\nCannot be undone!"):
                        success, msg = delete_user_from_db(uid)
                        if success: messagebox.showinfo("Success", msg); load_users()
                        else:       messagebox.showerror("Error", msg)
                create_icon_button(table_frame, "Delete", "🗑️", "#F44336", delete_user, idx, 3)
            else:
                admin_lbl = Label(table_frame, text="Cannot Delete Admin", bg=row_color,
                                  fg="#FF6347", font=("Arial", 10, "italic"), width=20, relief="ridge")
                admin_lbl.grid(row=idx, column=3, padx=2, pady=2)
                admin_lbl.bind("<Enter>", lambda e, l=admin_lbl: l.config(bg="#FFCCCB", fg="#E04141"))
                admin_lbl.bind("<Leave>", lambda e, l=admin_lbl, bg=row_color: l.config(bg=bg, fg="#FF6347"))

    load_users()

    # ── Refresh button ─────────────────────────────────────────────
    button_frame = Frame(content_frame, bg="#5D48B8")
    button_frame.pack(pady=10)
    create_icon_button(button_frame, "Refresh List", "🔄", "#4CAF50", load_users, use_pack=True)

    # ── Instructions ──────────────────────────────────────────────
    instructions_frame = Frame(content_frame, bg="#5D48B8")
    instructions_frame.pack(pady=20)
    Label(instructions_frame,
          text="Instructions:\n"
               "1. View all registered users in the table above\n"
               "2. Regular users can be deleted by clicking 'Delete'\n"
               "3. Admin accounts cannot be deleted (security)\n"
               "4. Click 'Refresh List' to update\n"
               "5. Role colors: Red = Admin, Green = User",
          bg="#5D48B8", fg="white", font=("Arial", 10), justify=LEFT).pack()

    root.mainloop()


if __name__ == "__main__":
    run()