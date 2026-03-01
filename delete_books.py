from tkinter import *
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part, make_back_btn, icon_btn
from database_operations import get_all_books, delete_book_from_db


class DeleteBooksPage(Frame):
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

        tf = Frame(cf, bg="#5D48B8"); tf.pack(pady=30)
        Label(tf, text="🗑️", font=("Arial", 40), bg="#5D48B8", fg="white").pack(side=LEFT, padx=10)
        Label(tf, text="Delete Book", font=("Arial", 24, "bold"),
              bg="#5D48B8", fg="white").pack(side=LEFT)

        # Table card
        card = Frame(cf, bg="#3d2e8a", relief="groove", bd=2)
        card.pack(pady=10, padx=60, fill=X)

        bf = Frame(card, bg="#3d2e8a"); bf.pack(pady=(15, 5))
        icon_btn(bf, "Refresh List", "🔄", "#4CAF50", self.load)

        self.table = Frame(card, bg="#0d1b4c"); self.table.pack(pady=10, padx=20)
        for i, h in enumerate(["Book ID", "Book Name", "Author", "Year", "Quantity"]):
            Label(self.table, text=h, bg="#0d1b4c", fg="white", font=("Arial", 12, "bold"),
                  width=16, relief="ridge", padx=5, pady=5).grid(row=0, column=i, padx=1, pady=1)

        self.load()

        # Delete row
        df = Frame(card, bg="#3d2e8a"); df.pack(pady=20)
        Label(df, text="Book ID to delete:", bg="#3d2e8a", fg="white",
              font=("Arial", 13)).pack(side=LEFT, padx=(0, 10))
        self.bid_e = Entry(df, font=("Arial", 13), bg="#e6e6e6", width=16)
        self.bid_e.pack(side=LEFT, padx=(0, 15))
        icon_btn(df, "Delete Book", "❌", "#F44336", self.delete)

        Label(card, text="Books currently issued cannot be deleted.",
              bg="#3d2e8a", fg="#ffaaaa", font=("Arial", 10)).pack(pady=(0, 15))

    def load(self):
        for w in self.table.grid_slaves():
            if int(w.grid_info()["row"]) > 0: w.destroy()
        books = get_all_books()
        if not books:
            Label(self.table, text="No books found", bg="#0d1b4c", fg="white",
                  font=("Arial", 12), width=80).grid(row=1, column=0, columnspan=5, pady=10); return
        for idx, b in enumerate(books, 1):
            rc = "#1a237e" if idx % 2 == 0 else "#283593"
            for col, key in enumerate(['book_id','title','author','published_year','quantity']):
                Label(self.table, text=b[key], bg=rc, fg="white", font=("Arial", 11),
                      width=16, relief="ridge", padx=5, pady=4
                      ).grid(row=idx, column=col, padx=1, pady=1)

    def delete(self):
        bid = self.bid_e.get().strip()
        if not bid: messagebox.showerror("Error", "Enter a Book ID!"); return
        try:
            if messagebox.askyesno("Confirm", f"Delete Book ID {bid}? Cannot be undone!"):
                ok, msg = delete_book_from_db(int(bid))
                if ok: messagebox.showinfo("Deleted", msg); self.bid_e.delete(0, END); self.load()
                else:  messagebox.showerror("Error", msg)
        except ValueError: messagebox.showerror("Error", "Book ID must be a number!")