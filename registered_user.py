from tkinter import *
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part, make_back_btn, icon_btn
from database_operations import get_all_users, delete_user_from_db


class RegisteredUserPage(Frame):
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
        Label(tf, text="👤", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
        Label(tf, text="Registered Users", font=("Arial", 24, "bold"),
              bg="#5D48B8", fg="white").pack(side=LEFT)

        card = Frame(cf, bg="#3d2e8a", relief="groove", bd=2)
        card.pack(pady=10, padx=60, fill=X)

        bf = Frame(card, bg="#3d2e8a"); bf.pack(pady=(15, 5))
        icon_btn(bf, "Refresh", "🔄", "#4CAF50", self.load)

        self.table = Frame(card, bg="#0d1b4c"); self.table.pack(pady=10, padx=20)
        for i, h in enumerate(["User ID", "Username", "Role", "Action"]):
            Label(self.table, text=h, bg="#0d1b4c", fg="white", font=("Arial", 12, "bold"),
                  width=22, relief="ridge", padx=5, pady=5).grid(row=0, column=i, padx=1, pady=1)

        Label(card, text="Admin accounts are protected and cannot be deleted.",
              bg="#3d2e8a", fg="#ffaaaa", font=("Arial", 10)).pack(pady=(5, 15))
        self.load()

    def load(self):
        for w in self.table.grid_slaves():
            if int(w.grid_info()["row"]) > 0: w.destroy()
        users = get_all_users()
        if not users:
            Label(self.table, text="No users found", bg="#0d1b4c", fg="white",
                  font=("Arial", 12), width=88).grid(row=1, column=0, columnspan=4); return
        for idx, u in enumerate(users, 1):
            rc  = "#1a237e" if idx % 2 == 0 else "#283593"
            rfc = "#ff6666" if u['role'] == 'admin' else "#80ff80"
            Label(self.table, text=u['user_id'],  bg=rc, fg="white", width=22,
                  relief="ridge", padx=5, pady=5).grid(row=idx, column=0, padx=1, pady=1)
            Label(self.table, text=u['username'],  bg=rc, fg="white", width=22,
                  relief="ridge", padx=5, pady=5).grid(row=idx, column=1, padx=1, pady=1)
            Label(self.table, text=u['role'].upper(), bg=rc, fg=rfc,
                  font=("Arial", 11, "bold"), width=22, relief="ridge",
                  padx=5, pady=5).grid(row=idx, column=2, padx=1, pady=1)
            if u['role'] != 'admin':
                Button(self.table, text="🗑 Delete", bg="#F44336", fg="white",
                       font=("Arial", 11), width=20, relief="ridge", cursor="hand2",
                       command=lambda uid=u['user_id']: self.del_user(uid)
                       ).grid(row=idx, column=3, padx=1, pady=1)
            else:
                Label(self.table, text="🔒 Protected", bg=rc, fg="#aaa",
                      width=22, relief="ridge", padx=5, pady=5).grid(
                    row=idx, column=3, padx=1, pady=1)

    def del_user(self, uid):
        if messagebox.askyesno("Confirm", f"Delete user ID {uid}?"):
            ok, msg = delete_user_from_db(uid)
            if ok: messagebox.showinfo("Deleted", msg); self.load()
            else:  messagebox.showerror("Error", msg)