from tkinter import *
from function_header_body import header_part, body_part, make_back_btn, icon_btn
from database_operations import get_all_history


class HistoryPage(Frame):
    def __init__(self, parent, controller, username="Guest"):
        super().__init__(parent)
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

        make_back_btn(cf, controller)

        tf = Frame(cf, bg="#5D48B8"); tf.pack(pady=25)
        Label(tf, text="📋", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
        Label(tf, text="Issue History", font=("Arial", 24, "bold"),
              bg="#5D48B8", fg="white").pack(side=LEFT)

        card = Frame(cf, bg="#3d2e8a", relief="groove", bd=2)
        card.pack(pady=10, padx=40, fill=X)

        bf = Frame(card, bg="#3d2e8a"); bf.pack(pady=(15, 5))
        icon_btn(bf, "Refresh", "🔄", "#2196F3", self.load)

        # Table with horiz scrollbar
        tw = Frame(card, bg="#3d2e8a"); tw.pack(pady=10, padx=20, fill=BOTH, expand=True)
        tc = Canvas(tw, bg="#5D48B8", height=400, highlightthickness=0)
        tc.pack(side=LEFT, fill=BOTH, expand=True)
        vsb2 = Scrollbar(tw, orient=VERTICAL, command=tc.yview); vsb2.pack(side=RIGHT, fill=Y)
        hsb  = Scrollbar(card, orient=HORIZONTAL, command=tc.xview); hsb.pack(fill=X, padx=20)
        tc.configure(yscrollcommand=vsb2.set, xscrollcommand=hsb.set)
        self.inner = Frame(tc, bg="#5D48B8")
        tc.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: tc.configure(scrollregion=tc.bbox("all")))

        self.cols   = ["Issue ID", "Username", "Book Title", "Issue Date", "Return Date", "Status"]
        self.widths = [10, 18, 22, 14, 14, 14]
        for i, (h, w) in enumerate(zip(self.cols, self.widths)):
            Label(self.inner, text=h, bg="#0d1b4c", fg="white", font=("Arial", 12, "bold"),
                  width=w, relief="ridge", padx=5, pady=5).grid(row=0, column=i, padx=1, pady=1)

        Label(card, text="Status: 🟢 Returned   🟠 Not Returned",
              bg="#3d2e8a", fg="white", font=("Arial", 10)).pack(pady=(5, 15))
        self.load()

    def load(self):
        for w in self.inner.grid_slaves():
            if int(w.grid_info()["row"]) > 0: w.destroy()
        records = get_all_history()
        if not records:
            Label(self.inner, text="No records found", bg="#5D48B8", fg="white",
                  font=("Arial", 14)).grid(row=1, column=0, columnspan=6, pady=20); return
        for idx, r in enumerate(records, 1):
            rc = "#1a237e" if idx % 2 == 0 else "#283593"
            vals = [r['issue_id'], r['user_name'], r['book_name'],
                    r['issue_date'], r['return_date'], r['status']]
            for col, (val, w) in enumerate(zip(vals, self.widths)):
                is_s = col == 5
                fg = ("#80ff80" if r['status'] == "Returned" else "#FF9800") if is_s else "white"
                Label(self.inner, text=str(val), bg=rc, fg=fg,
                      font=("Arial", 11, "bold" if is_s else "normal"),
                      width=w, relief="ridge", padx=5, pady=4
                      ).grid(row=idx, column=col, padx=1, pady=1)