from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part, make_back_btn
from database_operations import add_issue_record, return_book, get_active_issues


class RecordsPage(Frame):
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
        cf = Frame(canvas, bg="#0d1b4c")
        cw = canvas.create_window((0,0), window=cf, anchor="nw")
        cf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))

        def _scroll(e): canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        def _bind(e):   canvas.bind_all("<MouseWheel>", _scroll)
        def _unbind(e): canvas.unbind_all("<MouseWheel>")
        canvas.bind("<Enter>", _bind)
        canvas.bind("<Leave>", _unbind)
        cf.bind("<Enter>", _bind)
        cf.bind("<Leave>", _unbind)

        make_back_btn(cf, controller)

        # Title
        tf = Frame(cf, bg="#5D48B8"); tf.pack(pady=20)
        Label(tf, text="📊", font=("Arial",40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
        Label(tf, text="Book Records", font=("Arial",24,"bold"),
              bg="#5D48B8", fg="white").pack(side=LEFT)

        def section(title):
            s = Frame(cf, bg="#3d2e8a", relief="groove", bd=2)
            s.pack(pady=12, padx=30, fill=X)
            Label(s, text=title, bg="#3d2e8a", fg="white",
                  font=("Arial",14,"bold")).pack(pady=10)
            return s

        def form_row(parent, icon, lbl, row):
            lf = Frame(parent, bg="#3d2e8a"); lf.grid(row=row, column=0, padx=20, pady=8, sticky=W)
            Label(lf, text=icon, font=("Arial",14), bg="#3d2e8a", fg="white").pack(side=LEFT, padx=(0,8))
            Label(lf, text=lbl, font=("Arial",13), bg="#3d2e8a", fg="white").pack(side=LEFT)
            e = Entry(parent, font=("Arial",13), width=30); e.grid(row=row, column=1, padx=20, pady=8)
            return e

        # Issue section
        isf = section("📖  Issue Book")
        ff = Frame(isf, bg="#3d2e8a"); ff.pack()
        e_uid = form_row(ff, "👤", "User ID:", 0)
        e_bid = form_row(ff, "📕", "Book ID:", 1)

        def do_issue():
            uid, bid = e_uid.get().strip(), e_bid.get().strip()
            if not uid or not bid: messagebox.showerror("Error","Enter User ID and Book ID!"); return
            try:
                ok, msg = add_issue_record(int(uid), int(bid))
                if ok: messagebox.showinfo("Success",msg); e_uid.delete(0,END); e_bid.delete(0,END); self.refresh()
                else:  messagebox.showerror("Error",msg)
            except ValueError: messagebox.showerror("Error","IDs must be numbers!")

        Button(isf, text="📤 Issue Book", font=("Arial",12,"bold"),
               bg="#4CAF50", fg="white", padx=20, pady=8,
               cursor="hand2", command=do_issue).pack(pady=10)

        # Return section
        rtf = section("📥  Return Book")
        rff = Frame(rtf, bg="#3d2e8a"); rff.pack()
        e_iid = form_row(rff, "🆔", "Issue ID:", 0)

        def do_return():
            iid = e_iid.get().strip()
            if not iid: messagebox.showerror("Error","Enter Issue ID!"); return
            try:
                if messagebox.askyesno("Confirm", f"Return Issue ID {iid}?"):
                    ok, msg = return_book(int(iid))
                    if ok: messagebox.showinfo("Success",msg); e_iid.delete(0,END); self.refresh()
                    else:  messagebox.showerror("Error",msg)
            except ValueError: messagebox.showerror("Error","Issue ID must be a number!")

        Button(rtf, text="📥 Return Book", font=("Arial",12,"bold"),
               bg="#FF5722", fg="white", padx=20, pady=8,
               cursor="hand2", command=do_return).pack(pady=10)

        # Active issues
        aif = section("📊  Currently Issued Books")
        tree_f = Frame(aif, bg="#3d2e8a"); tree_f.pack(fill=BOTH, expand=True, padx=10, pady=8)

        self.tree = ttk.Treeview(tree_f,
            columns=("Issue ID","User","Book Title","Issue Date"),
            show="headings", height=8)
        for col, w in [("Issue ID",100),("User",200),("Book Title",300),("Issue Date",150)]:
            self.tree.heading(col, text=col); self.tree.column(col, width=w, anchor="center")
        vsb = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True); vsb.pack(side=RIGHT, fill=Y)

        s = ttk.Style()
        s.configure("Treeview", rowheight=26)
        s.map("Treeview", background=[("selected","#5D48B8")])

        Button(aif, text="🔄 Refresh", font=("Arial",12,"bold"),
               bg="#2196F3", fg="white", padx=20, pady=8,
               cursor="hand2", command=self.refresh).pack(pady=10)

        self.refresh()

    def refresh(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        issues = get_active_issues()
        if not issues:
            self.tree.insert("","end",values=("—","No active issues","",""))
        else:
            for r in issues:
                self.tree.insert("","end",
                    values=(r['issue_id'],r['username'],r['book_name'],r['issue_date']))