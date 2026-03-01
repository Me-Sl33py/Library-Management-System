from tkinter import *
from function_header_body import header_part, body_part


class HomePage(Frame):
    def __init__(self, parent, controller, username="Guest"):
        super().__init__(parent)
        header_part(self, username=username,
                    on_profile_click=lambda: controller.show_frame("ProfilePage"))
        body = body_part(self)

        # Scrollable canvas fills body
        main = Frame(body, bg="#0d1b4c"); main.pack(fill=BOTH, expand=True)
        canvas = Canvas(main, bg="#0d1b4c", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        sb = Scrollbar(main, orient=VERTICAL, command=canvas.yview); sb.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=sb.set)
        cf = Frame(canvas, bg="#0d1b4c")
        cw = canvas.create_window((0, 0), window=cf, anchor="nw")
        cf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Button grid — centred in cf
        container = Frame(cf, bg="#0d1b4c", width=1100, height=620)
        container.pack(expand=True, pady=40)
        container.pack_propagate(False)
        for i in range(3): container.columnconfigure(i, weight=1, uniform="col")
        for i in range(2): container.rowconfigure(i,    weight=1, uniform="row")

        buttons = [
            {"text": "Add / Update\nBook", "icon": "📖", "color": "#4CAF50", "page": "AddUpdatePage"},
            {"text": "Delete Books",        "icon": "🗑️", "color": "#f44336", "page": "DeleteBooksPage"},
            {"text": "Available Books",     "icon": "📚", "color": "#2196F3", "page": "AvailableBooksPage"},
            {"text": "Register Users",      "icon": "👤", "color": "#FF9800", "page": "RegisteredUserPage"},
            {"text": "History",             "icon": "📋", "color": "#9C27B0", "page": "HistoryPage"},
            {"text": "Records",             "icon": "📊", "color": "#009688", "page": "RecordsPage"},
        ]

        for idx, btn in enumerate(buttons):
            r, c = idx // 3, idx % 3
            bf = Frame(container, bg="white", relief="raised", bd=2)
            bf.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
            il = Label(bf, text=btn["icon"], font=("Arial", 40), bg="white", fg=btn["color"])
            il.pack(pady=(20, 10))
            tl = Label(bf, text=btn["text"], font=("Arial", 14, "bold"), bg="white", fg="black")
            tl.pack(pady=(0, 20))

            def on_click(e, p=btn["page"]): controller.show_frame(p)
            def on_e(e, f=bf, i=il, t=tl): f.config(bg="aqua"); i.config(bg="aqua"); t.config(bg="aqua")
            def on_l(e, f=bf, i=il, t=tl): f.config(bg="white"); i.config(bg="white"); t.config(bg="white")
            for w in (bf, il, tl):
                w.bind("<Button-1>", on_click)
                w.bind("<Enter>", on_e)
                w.bind("<Leave>", on_l)