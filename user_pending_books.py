from tkinter import *
from function_header_body import header_part, body_part, make_back_btn, icon_btn
from database_operations import get_user_pending_books


class UserPendingBooksPage(Frame):
    def __init__(self, parent, controller, username="Guest"):
        super().__init__(parent)
        self.username = username
        header_part(self, username=username,
                    on_profile_click=lambda: controller.show_frame("UserProfilePage"))
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

        make_back_btn(cf, controller, dest="UserHomePage")

        tf = Frame(cf, bg="#5D48B8"); tf.pack(pady=25)
        Label(tf, text="⏳", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
        Label(tf, text="Pending Books", font=("Arial", 24, "bold"),
              bg="#5D48B8", fg="white").pack(side=LEFT)

        card = Frame(cf, bg="#3d2e8a", relief="groove", bd=2)
        card.pack(pady=10, padx=60, fill=X)

        bf = Frame(card, bg="#3d2e8a"); bf.pack(pady=(15, 5))
        icon_btn(bf, "Refresh", "🔄", "#FF9800", self.load)

        self.table = Frame(card, bg="#0d1b4c"); self.table.pack(pady=10, padx=20)
        for i, (h, w) in enumerate(zip(["Issue ID", "Book Title", "Issue Date"], [10, 35, 15])):
            Label(self.table, text=h, bg="#0d1b4c", fg="white", font=("Arial", 12, "bold"),
                  width=w, relief="ridge", padx=5, pady=5).grid(row=0, column=i, padx=1, pady=1)
        self.cw = [10, 35, 15]

        Label(card, text="Return them at the front desk or use Renew Book to extend.",
              bg="#3d2e8a", fg="white", font=("Arial", 10)).pack(pady=(5, 15))
        self.load()

    def load(self):
        for w in self.table.grid_slaves():
            if int(w.grid_info()["row"]) > 0: w.destroy()
        records = get_user_pending_books(self.username)
        if not records:
            Label(self.table, text="✅  No pending books — all clear!",
                  bg="#0d1b4c", fg="#80ff80", font=("Arial", 13), width=60
                  ).grid(row=1, column=0, columnspan=3, pady=20); return
        for idx, r in enumerate(records, 1):
            rc = "#1a237e" if idx % 2 == 0 else "#283593"
            for col, (key, w) in enumerate(zip(['issue_id','book_name','issue_date'], self.cw)):
                Label(self.table, text=r[key], bg=rc, fg="white", font=("Arial", 11),
                      width=w, relief="ridge", padx=5, pady=4
                      ).grid(row=idx, column=col, padx=1, pady=1)