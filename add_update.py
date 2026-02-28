from tkinter import *
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part
from database_operations import add_book_to_db, update_book_in_db


def open_page(root, module_name):
    root.destroy()
    import importlib
    importlib.import_module(module_name).run()


def run():
    root = Tk()
    root.title("Library Management System - Add/Update Book")
    root.geometry("1220x900")
    root.iconbitmap("logo_icon.ico")

    header = header_part(root)
    body   = body_part(root)

    # ── Scrollable setup ───────────────────────────────────────────
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
    # ✅ Inside content_frame using pack — fixes place vs pack conflict
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
    Label(title_frame, text="📖", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
    Label(title_frame, text="Add / Update Book", bg="#5D48B8", fg="white",
          font=("Arial", 24, "bold")).pack(side=LEFT)

    # ── Form ───────────────────────────────────────────────────────
    form_frame = Frame(content_frame, bg="#5D48B8")
    form_frame.pack(pady=20)

    def create_form_row(icon, label_text, row):
        lf = Frame(form_frame, bg="#5D48B8")
        lf.grid(row=row, column=0, padx=20, pady=15, sticky="w")
        Label(lf, text=icon, font=("Arial", 16), bg="#5D48B8", fg="white").pack(side=LEFT, padx=(0, 10))
        Label(lf, text=label_text, bg="#5D48B8", fg="white", font=("Arial", 14)).pack(side=LEFT)
        entry = Entry(form_frame, font=("Arial", 14), width=40)
        entry.grid(row=row, column=1, padx=20, pady=15)
        return entry

    book_id_entry   = create_form_row("🆔", "Book ID (for update only):", 0)
    book_name_entry = create_form_row("📕", "Book Name:",                 1)
    author_entry    = create_form_row("✍️",  "Author:",                   2)
    year_entry      = create_form_row("📅", "Published Year:",            3)
    quantity_entry  = create_form_row("🔢", "Quantity:",                  4)

    # ── Helpers ────────────────────────────────────────────────────
    def clear_form():
        for e in (book_id_entry, book_name_entry, author_entry, year_entry, quantity_entry):
            e.delete(0, END)

    def add_book():
        name     = book_name_entry.get().strip()
        author   = author_entry.get().strip()
        year     = year_entry.get().strip()
        quantity = quantity_entry.get().strip()
        if not all([name, author, year, quantity]):
            messagebox.showerror("Error", "All fields except Book ID are required!"); return
        try:
            y, q = int(year), int(quantity)
            if y < 0:   messagebox.showerror("Error", "Year must be positive!"); return
            if q <= 0:  messagebox.showerror("Error", "Quantity must be > 0!"); return
            if add_book_to_db(name, author, y, q):
                messagebox.showinfo("Success", "Book added successfully!"); clear_form()
            else:
                messagebox.showerror("Error", "Failed to add book!")
        except ValueError:
            messagebox.showerror("Error", "Year and Quantity must be numbers!")

    def update_book():
        book_id  = book_id_entry.get().strip()
        name     = book_name_entry.get().strip()
        author   = author_entry.get().strip()
        year     = year_entry.get().strip()
        quantity = quantity_entry.get().strip()
        if not book_id:
            messagebox.showerror("Error", "Book ID required for update!"); return
        if not all([name, author, year, quantity]):
            messagebox.showerror("Error", "All fields are required!"); return
        try:
            bid, y, q = int(book_id), int(year), int(quantity)
            if y < 0:  messagebox.showerror("Error", "Year must be positive!"); return
            if q < 0:  messagebox.showerror("Error", "Quantity must be >= 0!"); return
            if messagebox.askyesno("Confirm", f"Update Book ID {bid}?"):
                success, msg = update_book_in_db(bid, name, author, y, q)
                if success: messagebox.showinfo("Success", msg); clear_form()
                else:       messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Book ID, Year and Quantity must be numbers!")

    # ── Buttons ────────────────────────────────────────────────────
    def create_icon_button(parent, text, icon, color, command):
        bf = Frame(parent, bg="white", relief="raised", bd=2)
        bf.pack(side=LEFT, padx=10)
        il = Label(bf, text=icon, font=("Arial", 20), bg="white", fg=color)
        il.pack(side=LEFT, padx=10)
        tl = Label(bf, text=text, font=("Arial", 14, "bold"), bg="white", fg="black")
        tl.pack(side=LEFT, padx=(0, 10))
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

    button_frame = Frame(content_frame, bg="#5D48B8")
    button_frame.pack(pady=30)
    create_icon_button(button_frame, "Add Book",    "➕", "#4CAF50", add_book)
    create_icon_button(button_frame, "Update Book", "✏️", "#2196F3", update_book)
    create_icon_button(button_frame, "Clear Form",  "🗑️", "#FF9800", clear_form)

    # ── Instructions ──────────────────────────────────────────────
    instructions_frame = Frame(content_frame, bg="#5D48B8")
    instructions_frame.pack(pady=20)
    Label(instructions_frame,
          text="Instructions:\n"
               "• To ADD: Leave Book ID empty, fill other fields, click 'Add Book'\n"
               "• To UPDATE: Enter Book ID, fill all fields, click 'Update Book'\n"
               "• To CLEAR: Click 'Clear Form'",
          bg="#5D48B8", fg="white", font=("Arial", 10), justify=LEFT).pack()

    book_name_entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    run()