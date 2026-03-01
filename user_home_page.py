from tkinter import *
from function_header_body import header_part, body_part


class UserHomePage(Frame):
    def __init__(self, parent, controller, username="Guest"):
        super().__init__(parent)
        header_part(self, username=username,
                    on_profile_click=lambda: controller.show_frame("UserProfilePage"))
        body = body_part(self)

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

        Label(cf, text=f"Welcome, {username}! 👋", font=("Arial", 16, "bold"),
              bg="#0d1b4c", fg="white").pack(pady=(25, 4))
        Label(cf, text="What would you like to do today?",
              font=("Arial", 12), bg="#0d1b4c", fg="#a0b0d0").pack()

        container = Frame(cf, bg="#0d1b4c", width=900, height=500)
        container.pack(expand=True, pady=30)
        container.pack_propagate(False)
        for i in range(2): container.columnconfigure(i, weight=1, uniform="col")
        for i in range(2): container.rowconfigure(i,    weight=1, uniform="row")

        buttons = [
            {"text": "Available Books",  "icon": "📚", "color": "#2196F3",
             "desc": "Browse all books",       "page": "UserAvailableBooksPage"},
            {"text": "Pending Books",    "icon": "⏳", "color": "#FF9800",
             "desc": "Books not returned",     "page": "UserPendingBooksPage"},
            {"text": "My History",       "icon": "📋", "color": "#9C27B0",
             "desc": "Your borrow history",    "page": "UserHistoryPage"},
            {"text": "Renew Book",       "icon": "🔄", "color": "#009688",
             "desc": "Extend return date +7d", "page": "UserRenewBookPage"},
        ]

        for idx, btn in enumerate(buttons):
            r, c = idx // 2, idx % 2
            bf = Frame(container, bg="white", relief="raised", bd=2)
            bf.grid(row=r, column=c, padx=20, pady=20, sticky="nsew")
            Frame(bf, bg=btn["color"], height=6).pack(fill=X)
            il = Label(bf, text=btn["icon"], font=("Arial", 44), bg="white", fg=btn["color"])
            il.pack(pady=(15, 5))
            tl = Label(bf, text=btn["text"], font=("Arial", 14, "bold"), bg="white", fg="black")
            tl.pack()
            dl = Label(bf, text=btn["desc"], font=("Arial", 10), bg="white", fg="#666")
            dl.pack(pady=(2, 15))
            ws = (bf, il, tl, dl)
            def on_click(e, p=btn["page"]): controller.show_frame(p)
            def on_e(e, w=ws, col=btn["color"]):
                for x in w: x.config(bg=col)
                w[2].config(fg="white"); w[3].config(fg="white")
            def on_l(e, w=ws):
                for x in w: x.config(bg="white")
                w[2].config(fg="black"); w[3].config(fg="#666")
            for w in ws:
                w.bind("<Button-1>", on_click)
                w.bind("<Enter>", on_e)
                w.bind("<Leave>", on_l)