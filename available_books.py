from tkinter import *
from function_header_body import header_part, body_part
from database_operations import get_all_books, search_books


def open_page(root, module_name):
    root.destroy()
    import importlib
    importlib.import_module(module_name).run()


def run():
    root = Tk()
    root.title("Library Management System - Available Books")
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

    #   Back button                         
    # ✅ Inside content_frame using pack
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

    #   Title                            
    title_frame = Frame(content_frame, bg="#5D48B8")
    title_frame.pack(pady=30)
    Label(title_frame, text="📚", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
    Label(title_frame, text="Available Books", bg="#5D48B8", fg="white",
          font=("Arial", 24, "bold")).pack(side=LEFT)

    #   Search bar                         ─
    search_frame = Frame(content_frame, bg="#5D48B8")
    search_frame.pack(pady=20)
    Label(search_frame, text="Search:", bg="#5D48B8", fg="white",
          font=("Arial", 12)).pack(side=LEFT, padx=(0, 10))
    search_var = StringVar()
    search_entry = Entry(search_frame, textvariable=search_var, font=("Arial", 12), width=40)
    search_entry.pack(side=LEFT, padx=(0, 10))

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

    def search_books_action():
        term = search_var.get().strip()
        display_books(search_books(term) if term else get_all_books())

    def refresh_action():
        search_var.set("")
        display_books(get_all_books())

    create_icon_button(search_frame, "Search",  "🔍", "#4CAF50", search_books_action)
    create_icon_button(search_frame, "Refresh", "🔄", "#2196F3", refresh_action)

    #   Table                            
    table_frame = Frame(content_frame, bg="#5D48B8")
    table_frame.pack(pady=20, padx=20)

    table_canvas = Canvas(table_frame, bg="#5D48B8", width=800, height=400, highlightthickness=0)
    table_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    table_scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=table_canvas.yview)
    table_scrollbar.pack(side=RIGHT, fill=Y)
    table_canvas.configure(yscrollcommand=table_scrollbar.set)

    inner_table_frame = Frame(table_canvas, bg="#5D48B8")
    table_canvas.create_window((0, 0), window=inner_table_frame, anchor="nw")

    def update_table_scrollregion(event=None):
        table_canvas.configure(scrollregion=table_canvas.bbox("all"))
    inner_table_frame.bind("<Configure>", update_table_scrollregion)

    for i, h in enumerate(["Book ID", "Book Name", "Author", "Year", "Quantity"]):
        Label(inner_table_frame, text=h, bg="#0d1b4c", fg="white",
              font=("Arial", 12, "bold"), width=20, relief="ridge",
              padx=5, pady=5).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

    def display_books(books):
        for widget in inner_table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        if not books:
            Label(inner_table_frame, text="No books found", bg="#5D48B8",
                  fg="white", font=("Arial", 14)).grid(row=1, column=0, columnspan=5, pady=20)
            return
        for idx, book in enumerate(books, start=1):
            row_color = "#1a237e" if idx % 2 == 0 else "#283593"
            for col, key in enumerate(['book_id', 'title', 'author', 'published_year', 'quantity']):
                Label(inner_table_frame, text=book[key], bg=row_color, fg="white",
                      font=("Arial", 11), width=20, relief="ridge",
                      padx=5, pady=5).grid(row=idx, column=col, sticky="nsew", padx=1, pady=1)
        for i in range(5):
            inner_table_frame.grid_columnconfigure(i, weight=1)

    display_books(get_all_books())

    #   Stats                            
    stats_frame = Frame(content_frame, bg="#5D48B8")
    stats_frame.pack(pady=20)
    stats_label = Label(stats_frame, text="", bg="#5D48B8", fg="white", font=("Arial", 12, "bold"))
    stats_label.pack()

    def update_stats():
        books = get_all_books()
        total_qty = sum(b['quantity'] for b in books)
        stats_label.config(text=f"Total Books: {len(books)} | Total Copies: {total_qty}")
    update_stats()

    #   Instructions                        
    instructions_frame = Frame(content_frame, bg="#5D48B8")
    instructions_frame.pack(pady=20)
    Label(instructions_frame,
          text="Instructions:\n"
               "1. View all available books in the table above\n"
               "2. Use the search bar to find specific books\n"
               "3. Click 'Refresh' to see all books again\n"
               "4. This is a read-only view",
          bg="#5D48B8", fg="white", font=("Arial", 10), justify=LEFT).pack()

    search_entry.bind("<Return>", lambda e: search_books_action())
    search_entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    run()