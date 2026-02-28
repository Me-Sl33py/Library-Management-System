from tkinter import *
from function_header_body import header_part, body_part


def open_page(root, module_name):
    """
    Safely close current window and open another page.
    Every page file must expose a run() function.
    """
    root.destroy()
    import importlib
    mod = importlib.import_module(module_name)
    mod.run()


def run():
    root = Tk()
    root.title("Library Management System")
    root.geometry("1220x900")
    root.iconbitmap("logo_icon.ico")

    header = header_part(root)
    body   = body_part(root)

    # ── Main container ─────────────────────────────────────────────
    container = Frame(body, bg="#0d1b4c", width=1100, height=600)
    container.place(relx=0.5, rely=0.5, anchor=CENTER)
    container.pack_propagate(False)

    # ── Grid config ────────────────────────────────────────────────
    for i in range(3):
        container.columnconfigure(i, weight=1, uniform="col")
    for i in range(2):
        container.rowconfigure(i, weight=1, uniform="row")

    # ── Button definitions ─────────────────────────────────────────
    buttons = [
        {"text": "Add / Update\nBook", "icon": "📖", "color": "#4CAF50", "page": "add_update"},
        {"text": "Delete Books",        "icon": "🗑️", "color": "#f44336", "page": "delete_book"},
        {"text": "Available Books",     "icon": "📚", "color": "#2196F3", "page": "available_books"},
        {"text": "Register Users",      "icon": "👤", "color": "#FF9800", "page": "register_users"},
        {"text": "History",             "icon": "📋", "color": "#9C27B0", "page": "history_page"},
        {"text": "Records",             "icon": "📊", "color": "#009688", "page": "records_page"},
    ]

    # ── Build each card-button ─────────────────────────────────────
    for index, btn_info in enumerate(buttons):
        r = index // 3
        c = index % 3

        btn_frame = Frame(container, bg="white", relief="raised", bd=2)
        btn_frame.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")

        icon_label = Label(btn_frame, text=btn_info["icon"],
                           font=("Arial", 40), bg="white", fg=btn_info["color"])
        icon_label.pack(pady=(20, 10))

        text_label = Label(btn_frame, text=btn_info["text"],
                           font=("Arial", 14, "bold"), bg="white", fg="black")
        text_label.pack(pady=(0, 20))

        # ✅ default-arg trick — captures correct value per loop iteration
        def on_click(e, page=btn_info["page"]):
            open_page(root, page)

        def on_enter(e, f=btn_frame, i=icon_label, t=text_label):
            f.config(bg="aqua"); i.config(bg="aqua"); t.config(bg="aqua")

        def on_leave(e, f=btn_frame, i=icon_label, t=text_label):
            f.config(bg="white"); i.config(bg="white"); t.config(bg="white")

        for widget in (btn_frame, icon_label, text_label):
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>",    on_enter)
            widget.bind("<Leave>",    on_leave)

    root.mainloop()


if __name__ == "__main__":
    run()