from tkinter import *
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part
from database_operations import get_all_books, delete_book_from_db


def open_page(root, module_name):
    root.destroy()
    import importlib
    importlib.import_module(module_name).run()


def run():
    root = Tk()
    root.title("Library Management System - Delete Book")
    root.geometry("1220x900")
    root.iconbitmap("logo_icon.ico")

    header = header_part(root)
    body   = body_part(root)

    container = Frame(body, bg="#5D48B8")
    container.place(relx=0.5, rely=0.5, anchor=CENTER)

    canvas = Canvas(container, bg="#5D48B8", width=800, height=500)
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
    Label(title_frame, text="🗑️", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
    Label(title_frame, text="Delete Book", bg="#5D48B8", fg="white",
          font=("Arial", 24, "bold")).pack(side=LEFT)

    # ── Table ──────────────────────────────────────────────────────
    table_frame = Frame(content_frame, bg="#0d1b4c")
    table_frame.pack(pady=20, padx=20)

    for i, h in enumerate(["Book ID", "Book Name", "Author", "Year", "Quantity"]):
        Label(table_frame, text=h, bg="#0d1b4c", fg="white",
              font=("Arial", 12, "bold"), width=15, relief="ridge").grid(
            row=0, column=i, padx=2, pady=2)

    def load_books():
        for widget in table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        books = get_all_books()
        if not books:
            Label(table_frame, text="No books found", bg="#0d1b4c", fg="white",
                  font=("Arial", 12), width=75).grid(row=1, column=0, columnspan=5, pady=10)
            return
        for idx, book in enumerate(books, start=1):
            row_color = "#1a237e" if idx % 2 == 0 else "#283593"
            for col, key in enumerate(['book_id', 'title', 'author', 'published_year', 'quantity']):
                Label(table_frame, text=book[key], bg=row_color, fg="white",
                      font=("Arial", 11), width=15, relief="ridge").grid(
                    row=idx, column=col, padx=2, pady=2)

    load_books()

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
    button_frame.pack(pady=10)
    create_icon_button(button_frame, "Refresh List", "🔄", "#4CAF50", load_books)

    # ── Delete section ─────────────────────────────────────────────
    delete_frame = Frame(content_frame, bg="#5D48B8")
    delete_frame.pack(pady=30)
    Label(delete_frame, text="Enter Book ID to Delete:", bg="#5D48B8", fg="white",
          font=("Arial", 14)).pack(side=LEFT, padx=(0, 10))
    book_id_entry = Entry(delete_frame, font=("Arial", 14), width=20)
    book_id_entry.pack(side=LEFT, padx=(0, 20))

    def delete_book():
        book_id = book_id_entry.get().strip()
        if not book_id:
            messagebox.showerror("Error", "Please enter a Book ID!"); return
        try:
            bid = int(book_id)
            if messagebox.askyesno("Confirm Delete",
                                   f"Delete Book ID {bid}?\nThis cannot be undone!"):
                success, msg = delete_book_from_db(bid)
                if success:
                    messagebox.showinfo("Success", msg)
                    book_id_entry.delete(0, END)
                    load_books()
                else:
                    messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Book ID must be a number!")

    create_icon_button(delete_frame, "Delete Book", "❌", "#F44336", delete_book)

    # ── Instructions ──────────────────────────────────────────────
    instructions_frame = Frame(content_frame, bg="#5D48B8")
    instructions_frame.pack(pady=20)
    Label(instructions_frame,
          text="Instructions:\n"
               "1. View the book list above\n"
               "2. Enter the Book ID you want to delete\n"
               "3. Click 'Delete Book' to remove it\n"
               "4. Click 'Refresh List' to update the table",
          bg="#5D48B8", fg="white", font=("Arial", 10), justify=LEFT).pack()

    book_id_entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    run()