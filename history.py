from tkinter import *
from function_header_body import header_part, body_part
from database_operations import get_all_history


def open_page(root, module_name):
    root.destroy()
    import importlib
    importlib.import_module(module_name).run()


def run():
    root = Tk()
    root.title("Library Management System - Issue History")
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

    content_frame = Frame(canvas, bg="#0d1b4c", highlightthickness=0, relief="flat")
    container_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def resize_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(container_window, width=event.width)
    content_frame.bind("<Configure>", resize_canvas)
    canvas.bind("<Configure>", resize_canvas)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    #   Back button                         
    # ✅ Inside content_frame using pack — no more place conflict
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
    title_frame.pack(pady=20)
    Label(title_frame, text="📜", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
    Label(title_frame, text="Issue History", bg="#5D48B8", fg="white",
          font=("Arial", 24, "bold")).pack(side=LEFT)

    #   Table                            
    table_frame = Frame(content_frame, bg="#5D48B8")
    table_frame.pack(pady=20, padx=20)

    canvas_table = Canvas(table_frame, bg="#5D48B8", width=1000, highlightthickness=0, height=500)
    canvas_table.pack(side=LEFT, fill=BOTH, expand=True)
    sb_y = Scrollbar(table_frame, orient=VERTICAL,   command=canvas_table.yview)
    sb_x = Scrollbar(table_frame, orient=HORIZONTAL, command=canvas_table.xview)
    canvas_table.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
    sb_y.pack(side=RIGHT,  fill=Y)
    sb_x.pack(side=BOTTOM, fill=X)

    inner_table_frame = Frame(canvas_table, bg="#5D48B8")
    canvas_table.create_window((0, 0), window=inner_table_frame, anchor="nw")

    def update_table_scrollregion(event=None):
        canvas_table.configure(scrollregion=canvas_table.bbox("all"))
    inner_table_frame.bind("<Configure>", update_table_scrollregion)

    headers    = ["Issue ID", "User ID", "User Name", "Book Name", "Issue Date", "Return Date", "Status"]
    col_widths = [10, 10, 18, 20, 15, 15, 12]

    for i, h in enumerate(headers):
        Label(inner_table_frame, text=h, bg="#0d1b4c", fg="white",
              font=("Arial", 12, "bold"), width=col_widths[i],
              relief="ridge", padx=5, pady=5).grid(
            row=0, column=i, sticky="nsew", padx=1, pady=1)

    def display_history(records):
        for widget in inner_table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        if not records:
            Label(inner_table_frame, text="No records found", bg="#5D48B8",
                  fg="white", font=("Arial", 14)).grid(row=1, column=0, columnspan=7, pady=20)
            return
        keys = ['issue_id', 'user_id', 'user_name', 'book_name', 'issue_date', 'return_date', 'status']
        for idx, rec in enumerate(records, start=1):
            row_color = "#1a237e" if idx % 2 == 0 else "#283593"
            for col, key in enumerate(keys):
                Label(inner_table_frame, text=str(rec[key]), bg=row_color, fg="white",
                      font=("Arial", 11), width=col_widths[col],
                      relief="ridge", padx=5, pady=5).grid(
                    row=idx, column=col, sticky="nsew", padx=1, pady=1)

    display_history(get_all_history())

    #   Refresh button                       ─
    def refresh():
        display_history(get_all_history())

    Button(content_frame, text="🔄 Refresh List", font=("Arial", 12, "bold"),
           bg="#2196F3", fg="white", padx=20, pady=10,
           command=refresh, cursor="hand2").pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run()