from tkinter import *
from function_header_body import header_part, body_part, make_back_btn, icon_btn
from database_operations import get_all_books, search_books


class AvailableBooksPage(Frame):
    def __init__(self, parent, controller, username="Guest", back_dest="HomePage"):
        super().__init__(parent)
        self.back_dest = back_dest
        header_part(self, username=username,
                    on_profile_click=lambda: controller.show_frame("ProfilePage"))
        body = body_part(self)

        main = Frame(body, bg="#5D48B8"); main.pack(fill=BOTH, expand=True)
        canvas = Canvas(main, bg="#5D48B8", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        sb = Scrollbar(main, orient=VERTICAL, command=canvas.yview); sb.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=sb.set)
        cf = Frame(canvas, bg="#5D48B8")
        cw = canvas.create_window((0, 0), window=cf, anchor="nw")
        cf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        make_back_btn(cf, controller, dest=back_dest)

        tf = Frame(cf, bg="#5D48B8"); tf.pack(pady=25)
        Label(tf, text="📚", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
        Label(tf, text="Available Books", font=("Arial", 24, "bold"),
              bg="#5D48B8", fg="white").pack(side=LEFT)

        # Search bar
        sf = Frame(cf, bg="#5D48B8"); sf.pack(pady=12)
        Label(sf, text="Search:", bg="#5D48B8", fg="white",
              font=("Arial", 12)).pack(side=LEFT, padx=(0, 8))
        self.sv = StringVar()
        Entry(sf, textvariable=self.sv, font=("Arial", 12), bg="#e6e6e6",
              width=38).pack(side=LEFT, padx=(0, 10))
        self.sv.trace("w", lambda *a: self.show(self.sv.get()))
        icon_btn(sf, "Refresh", "🔄", "#2196F3",
                 lambda: [self.sv.set(""), self.show("")])

        # Table card
        card = Frame(cf, bg="#3d2e8a", relief="groove", bd=2)
        card.pack(pady=10, padx=60, fill=X)

        self.table = Frame(card, bg="#0d1b4c"); self.table.pack(pady=20, padx=20)
        for i, h in enumerate(["Book ID", "Book Name", "Author", "Year", "Quantity"]):
            Label(self.table, text=h, bg="#0d1b4c", fg="white", font=("Arial", 12, "bold"),
                  width=18, relief="ridge", padx=5, pady=5).grid(row=0, column=i, padx=1, pady=1)

        self.stats = Label(card, text="", bg="#3d2e8a", fg="white", font=("Arial", 11, "bold"))
        self.stats.pack(pady=(0, 15))

        self.show("")

    def show(self, term=""):
        for w in self.table.grid_slaves():
            if int(w.grid_info()["row"]) > 0: w.destroy()
        books = search_books(term) if term.strip() else get_all_books()
        if not books:
            Label(self.table, text="No books found", bg="#0d1b4c", fg="white",
                  font=("Arial", 12), width=90).grid(row=1, column=0, columnspan=5, pady=15)
            self.stats.config(text=""); return
        for idx, b in enumerate(books, 1):
            rc = "#1a237e" if idx % 2 == 0 else "#283593"
            for col, key in enumerate(['book_id','title','author','published_year','quantity']):
                Label(self.table, text=b[key], bg=rc, fg="white", font=("Arial", 11),
                      width=18, relief="ridge", padx=5, pady=4
                      ).grid(row=idx, column=col, padx=1, pady=1)
        total = sum(b['quantity'] for b in get_all_books())
        self.stats.config(text=f"Showing {len(books)} book(s)   |   Total copies: {total}")