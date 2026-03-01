from tkinter import *
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part, make_back_btn, icon_btn
from database_operations import add_book_to_db, update_book_in_db


class AddUpdatePage(Frame):
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

        # Title
        tf = Frame(cf, bg="#5D48B8"); tf.pack(pady=30)
        Label(tf, text="📖", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
        Label(tf, text="Add / Update Book", font=("Arial", 24, "bold"),
              bg="#5D48B8", fg="white").pack(side=LEFT)

        # Centred form card
        card = Frame(cf, bg="#3d2e8a", relief="groove", bd=2)
        card.pack(pady=10, padx=80, fill=X)

        ff = Frame(card, bg="#3d2e8a"); ff.pack(pady=20, padx=40)

        def row(icon, lbl, r):
            lf = Frame(ff, bg="#3d2e8a"); lf.grid(row=r, column=0, padx=10, pady=12, sticky=W)
            Label(lf, text=icon, font=("Arial", 16), bg="#3d2e8a", fg="white").pack(side=LEFT, padx=(0,8))
            Label(lf, text=lbl, font=("Arial", 13), bg="#3d2e8a", fg="white").pack(side=LEFT)
            e = Entry(ff, font=("Arial", 13), width=38, bg="#e6e6e6")
            e.grid(row=r, column=1, padx=20, pady=12)
            return e

        e_id = row("🆔", "Book ID (update only):", 0)
        e_nm = row("📕", "Book Name:",             1)
        e_au = row("✍️",  "Author:",               2)
        e_yr = row("📅", "Published Year:",        3)
        e_qt = row("🔢", "Quantity:",              4)

        def clear():
            for e in (e_id, e_nm, e_au, e_yr, e_qt): e.delete(0, END)

        def add():
            nm, au, yr, qt = e_nm.get().strip(), e_au.get().strip(), e_yr.get().strip(), e_qt.get().strip()
            if not all([nm, au, yr, qt]): messagebox.showerror("Error","All fields except ID required!"); return
            try:
                y, q = int(yr), int(qt)
                if y < 0: messagebox.showerror("Error","Year must be positive"); return
                if q <= 0: messagebox.showerror("Error","Quantity must be > 0"); return
                if add_book_to_db(nm, au, y, q): messagebox.showinfo("Success","Book added!"); clear()
                else: messagebox.showerror("Error","Failed to add book")
            except ValueError: messagebox.showerror("Error","Year and Quantity must be numbers")

        def update():
            bid, nm, au, yr, qt = (e_id.get().strip(), e_nm.get().strip(),
                e_au.get().strip(), e_yr.get().strip(), e_qt.get().strip())
            if not bid: messagebox.showerror("Error","Book ID required for update!"); return
            if not all([nm, au, yr, qt]): messagebox.showerror("Error","All fields required!"); return
            try:
                b, y, q = int(bid), int(yr), int(qt)
                if messagebox.askyesno("Confirm", f"Update Book ID {b}?"):
                    ok, msg = update_book_in_db(b, nm, au, y, q)
                    if ok: messagebox.showinfo("Success", msg); clear()
                    else:  messagebox.showerror("Error", msg)
            except ValueError: messagebox.showerror("Error","ID/Year/Quantity must be numbers")

        bf = Frame(card, bg="#3d2e8a"); bf.pack(pady=(5, 25))
        icon_btn(bf, "Add Book",    "➕", "#4CAF50", add)
        icon_btn(bf, "Update Book", "✏️", "#2196F3", update)
        icon_btn(bf, "Clear Form",  "🗑️", "#FF9800", clear)

        Label(cf, text="• ADD: leave Book ID blank   • UPDATE: fill Book ID",
              bg="#5D48B8", fg="white", font=("Arial", 10)).pack(pady=10)
        e_nm.focus_set()