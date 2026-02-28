from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part
from database_operations import add_issue_record, return_book, get_active_issues


def open_page(root, module_name):
    root.destroy()
    import importlib
    importlib.import_module(module_name).run()


def run():
    root = Tk()
    root.title("Library Management System - Book Records")
    root.geometry("1220x900")
    root.iconbitmap("logo_icon.ico")

    header = header_part(root)
    body   = body_part(root)

    main_container = Frame(body, bg="#5D48B8")
    main_container.pack(fill=BOTH, expand=True)

    canvas = Canvas(main_container, bg="#5D48B8", highlightthickness=0)
    scrollbar = Scrollbar(main_container, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    container = Frame(canvas, bg="#0d1b4c")
    container_window = canvas.create_window((0, 0), window=container, anchor="nw")

    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(container_window, width=event.width)
    container.bind("<Configure>", configure_scroll_region)
    canvas.bind("<Configure>",    configure_scroll_region)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ── Back button ────────────────────────────────────────────────
    # ✅ Inside container using pack — fixes place conflict, removes duplicate
    back_frame = Frame(container, bg="#a6093d", relief="raised", bd=2)
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
    title_frame = Frame(container, bg="#5D48B8")
    title_frame.pack(pady=20)
    Label(title_frame, text="📋", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
    Label(title_frame, text="Book Records", bg="#5D48B8", fg="white",
          font=("Arial", 24, "bold")).pack(side=LEFT)

    # ── Helpers ────────────────────────────────────────────────────
    def create_form_row(parent, icon, label_text, row):
        lf = Frame(parent, bg="#5D48B8")
        lf.grid(row=row, column=0, padx=20, pady=15, sticky="w")
        Label(lf, text=icon, font=("Arial", 16), bg="#5D48B8", fg="white").pack(side=LEFT, padx=(0, 10))
        Label(lf, text=label_text, bg="#5D48B8", fg="white", font=("Arial", 14)).pack(side=LEFT)
        entry = Entry(parent, font=("Arial", 14), width=40)
        entry.grid(row=row, column=1, padx=20, pady=15)
        return entry

    def create_button(parent, text, icon, color, command):
        return Button(parent, text=f"{icon} {text}", font=("Arial", 12, "bold"),
                      bg=color, fg="white", padx=20, pady=10, command=command, cursor="hand2")

    # ── Issue Book ─────────────────────────────────────────────────
    issue_frame = Frame(container, bg="#5D48B8", relief="groove", bd=2)
    issue_frame.pack(pady=20, padx=20, fill=X)
    Label(issue_frame, text="📖 Issue Book", bg="#5D48B8", fg="white",
          font=("Arial", 16, "bold")).pack(pady=10)
    issue_form_frame = Frame(issue_frame, bg="#5D48B8")
    issue_form_frame.pack(pady=10)
    issue_user_entry = create_form_row(issue_form_frame, "👤", "User ID:", 0)
    issue_book_entry = create_form_row(issue_form_frame, "📕", "Book ID:", 1)

    def on_issue_click():
        uid = issue_user_entry.get().strip()
        bid = issue_book_entry.get().strip()
        if not uid or not bid:
            messagebox.showerror("Error", "Please enter both User ID and Book ID!"); return
        try:
            success, msg = add_issue_record(int(uid), int(bid))
            if success:
                messagebox.showinfo("Success", msg)
                issue_user_entry.delete(0, END)
                issue_book_entry.delete(0, END)
                refresh_issues()
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "User ID and Book ID must be numbers!")

    create_button(issue_frame, "Issue Book", "📤", "#4CAF50", on_issue_click).pack(pady=10)

    # ── Return Book ────────────────────────────────────────────────
    return_frame = Frame(container, bg="#5D48B8", relief="groove", bd=2)
    return_frame.pack(pady=20, padx=20, fill=X)
    Label(return_frame, text="📥 Return Book", bg="#5D48B8", fg="white",
          font=("Arial", 16, "bold")).pack(pady=10)
    return_form_frame = Frame(return_frame, bg="#5D48B8")
    return_form_frame.pack(pady=10)
    return_issue_entry = create_form_row(return_form_frame, "🆔", "Issue ID:", 0)

    def on_return_click():
        iid = return_issue_entry.get().strip()
        if not iid:
            messagebox.showerror("Error", "Please enter Issue ID!"); return
        try:
            iid_int = int(iid)
            if messagebox.askyesno("Confirm Return", f"Return book for Issue ID {iid_int}?"):
                success, msg = return_book(iid_int)
                if success:
                    messagebox.showinfo("Success", msg)
                    return_issue_entry.delete(0, END)
                    refresh_issues()
                else:
                    messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Issue ID must be a number!")

    create_button(return_frame, "Return Book", "📥", "#FF5722", on_return_click).pack(pady=10)

    # ── Active Issues Table ────────────────────────────────────────
    active_frame = Frame(container, bg="#5D48B8", relief="groove", bd=2)
    active_frame.pack(pady=20, padx=20, fill=X)
    Label(active_frame, text="📊 Active Issues", bg="#5D48B8", fg="white",
          font=("Arial", 16, "bold")).pack(pady=10)

    tree_frame = Frame(active_frame, bg="#5D48B8")
    tree_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

    tree = ttk.Treeview(tree_frame,
                        columns=("Issue ID", "User", "Book Title", "Issue Date"),
                        show="headings", height=8)
    for col, w in [("Issue ID", 100), ("User", 200), ("Book Title", 300), ("Issue Date", 150)]:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    vsb = ttk.Scrollbar(tree_frame, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    vsb.pack(side=RIGHT,  fill=Y)
    hsb.pack(side=BOTTOM, fill=X)

    style = ttk.Style()
    style.configure("Treeview", background="white", foreground="black",
                    rowheight=25, fieldbackground="white")
    style.map("Treeview", background=[("selected", "#5D48B8")])

    def refresh_issues():
        for item in tree.get_children():
            tree.delete(item)
        issues = get_active_issues()
        if not issues:
            tree.insert("", "end", values=("No active issues", "", "", ""))
        else:
            for issue in issues:
                tree.insert("", "end", values=issue)

    create_button(active_frame, "Refresh List", "🔄", "#2196F3", refresh_issues).pack(pady=10)
    refresh_issues()

    root.mainloop()


if __name__ == "__main__":
    run()