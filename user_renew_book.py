from tkinter import *
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part, make_back_btn, icon_btn
from database_operations import get_user_pending_books, renew_book


class UserRenewBookPage(Frame):
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
        Label(tf, text="🔄", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
        Label(tf, text="Renew Book", font=("Arial", 24, "bold"),
              bg="#5D48B8", fg="white").pack(side=LEFT)

        # Reference table card
        ref_card = Frame(cf, bg="#3d2e8a", relief="groove", bd=2)
        ref_card.pack(pady=10, padx=60, fill=X)
        Label(ref_card, text="Your Currently Issued Books", bg="#3d2e8a", fg="#a8d8ff",
              font=("Arial", 13, "bold")).pack(pady=(15, 8))

        self.ref_table = Frame(ref_card, bg="#0d1b4c"); self.ref_table.pack(padx=20, pady=(0, 5))
        for i, (h, w) in enumerate(zip(["Issue ID", "Book Title", "Issue Date"], [10, 35, 15])):
            Label(self.ref_table, text=h, bg="#0d1b4c", fg="white", font=("Arial", 11, "bold"),
                  width=w, relief="ridge", padx=4, pady=4).grid(row=0, column=i, padx=1, pady=1)
        self.ref_w = [10, 35, 15]

        bf = Frame(ref_card, bg="#3d2e8a"); bf.pack(pady=(8, 15))
        icon_btn(bf, "Refresh", "🔄", "#009688", self.load_ref)
        self.load_ref()

        # Renew form card
        form = Frame(cf, bg="#3d2e8a", relief="groove", bd=2)
        form.pack(pady=10, padx=60, fill=X)
        Label(form, text="📝  Submit Renewal Request", bg="#3d2e8a", fg="white",
              font=("Arial", 14, "bold")).pack(pady=(18, 10))
        Label(form, text="Enter Issue ID to renew:", bg="#3d2e8a", fg="white",
              font=("Arial", 12)).pack()
        self.iid_e = Entry(form, font=("Arial", 14), bg="#e6e6e6", width=18)
        self.iid_e.pack(ipady=6, pady=(6, 10))

        self.result_lbl = Label(form, text="", bg="#3d2e8a", font=("Arial", 12, "bold"))
        self.result_lbl.pack()

        def do_renew():
            iid = self.iid_e.get().strip()
            if not iid: messagebox.showerror("Error", "Enter an Issue ID!"); return
            try:
                ok, msg = renew_book(self.username, int(iid))
                if ok:
                    self.result_lbl.config(text=f"✅  {msg}", fg="#80ff80")
                    self.iid_e.delete(0, END); self.load_ref()
                else:
                    self.result_lbl.config(text=f"❌  {msg}", fg="#ff8080")
            except ValueError: messagebox.showerror("Error", "Issue ID must be a number!")

        Button(form, text="🔄  Request Renewal", font=("Arial", 13, "bold"),
               bg="#009688", fg="white", padx=25, pady=10,
               cursor="hand2", command=do_renew).pack(pady=(10, 8))
        Label(form, text="ℹ️  Renewal extends your return period by 7 days.",
              bg="#3d2e8a", fg="#d0c8ff", font=("Arial", 10)).pack(pady=(0, 18))

    def load_ref(self):
        for w in self.ref_table.grid_slaves():
            if int(w.grid_info()["row"]) > 0: w.destroy()
        records = get_user_pending_books(self.username)
        if not records:
            Label(self.ref_table, text="✅  No pending books.", bg="#0d1b4c",
                  fg="#80ff80", font=("Arial", 12), width=60
                  ).grid(row=1, column=0, columnspan=3, pady=12); return
        for idx, r in enumerate(records, 1):
            rc = "#1a237e" if idx % 2 == 0 else "#283593"
            for col, (key, w) in enumerate(zip(['issue_id','book_name','issue_date'], self.ref_w)):
                Label(self.ref_table, text=r[key], bg=rc, fg="white", font=("Arial", 11),
                      width=w, relief="ridge", padx=4, pady=4
                      ).grid(row=idx, column=col, padx=1, pady=1)