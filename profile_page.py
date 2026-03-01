from tkinter import *
import tkinter.messagebox as messagebox
from function_header_body import header_part, body_part
import database_operations


class ProfilePage(Frame):
    def __init__(self, parent, controller, username="Guest"):
        super().__init__(parent)
        header_part(self, username=username,
                    on_profile_click=lambda: controller.show_frame("HomePage"))
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

        # Centred card
        card = Frame(cf, bg="#5D48B8", bd=2, relief="ridge")
        card.pack(pady=40, padx=200, fill=X)

        Label(card, text="👤  My Profile", font=("Arial", 22, "bold"),
              bg="#5D48B8", fg="white").pack(pady=(30, 5))
        Label(card, text=f"Logged in as:  {username}", font=("Arial", 13),
              bg="#5D48B8", fg="#d0c8ff").pack(pady=(0, 20))
        Frame(card, bg="white", height=1).pack(fill=X, padx=30)

        def field(lbl, show=None):
            Label(card, text=lbl, bg="#5D48B8", fg="white",
                  font=("Arial", 12), anchor="w").pack(fill=X, padx=60, pady=(12, 2))
            e = Entry(card, font=("Arial", 13), bg="#e6e6e6", show=show, width=35)
            e.pack(ipady=6, padx=60, fill=X); return e

        # ── Change Username ────────────────────────────────────────────
        Label(card, text="Change Username", font=("Arial", 14, "bold"),
              bg="#5D48B8", fg="#a8d8ff").pack(anchor="w", padx=60, pady=(20, 0))
        e_newname = field("New Username")
        e_cu_pass = field("Current Password (required)", show="*")

        def change_username():
            nm, cp = e_newname.get().strip(), e_cu_pass.get()
            if not nm or not cp: messagebox.showerror("Error", "Fill all fields."); return
            if nm == username:   messagebox.showerror("Error", "Same as current username."); return
            if not database_operations.verify_user_credentials(username, cp):
                messagebox.showerror("Error", "Incorrect password."); return
            if database_operations.get_user_by_username(nm):
                messagebox.showerror("Error", f"'{nm}' already taken."); return
            ok, msg = database_operations.update_username(username, nm)
            if ok:
                messagebox.showinfo("Done ✅", "Username changed.\nPlease log in again.")
                controller.sign_out()
            else: messagebox.showerror("Error", msg)

        Button(card, text="✏️  Update Username", font=("Arial", 12, "bold"),
               bg="#2196F3", fg="white", padx=20, pady=8,
               cursor="hand2", command=change_username).pack(pady=(10, 5))
        Frame(card, bg="white", height=1).pack(fill=X, padx=30, pady=(15, 0))

        # ── Change Password ────────────────────────────────────────────
        Label(card, text="Change Password", font=("Arial", 14, "bold"),
              bg="#5D48B8", fg="#a8d8ff").pack(anchor="w", padx=60, pady=(20, 0))
        e_cur  = field("Current Password",            show="*")
        e_new  = field("New Password (min 8 chars)",  show="*")
        e_conf = field("Confirm New Password",        show="*")

        sv = BooleanVar()
        def toggle():
            s = "" if sv.get() else "*"
            for e in (e_cur, e_new, e_conf, e_cu_pass): e.config(show=s)
        Checkbutton(card, text="Show Passwords", variable=sv, bg="#5D48B8", fg="white",
                    selectcolor="#5D48B8", activebackground="#5D48B8", font=("Arial", 11),
                    command=toggle).pack(anchor="w", padx=60, pady=(6, 0))

        def change_password():
            cp, np, cn = e_cur.get(), e_new.get(), e_conf.get()
            if not all([cp, np, cn]): messagebox.showerror("Error", "Fill all fields."); return
            if not database_operations.verify_user_credentials(username, cp):
                messagebox.showerror("Error", "Incorrect current password."); return
            if len(np) < 8: messagebox.showerror("Error", "Min 8 characters."); return
            if np == cp:    messagebox.showerror("Error", "Same as current password."); return
            if np != cn:    messagebox.showerror("Error", "Passwords don't match."); return
            ok, msg = database_operations.update_password(username, np)
            if ok:
                messagebox.showinfo("Done ✅", "Password changed!\nPlease log in again.")
                controller.sign_out()
            else: messagebox.showerror("Error", msg)

        Button(card, text="🔒  Update Password", font=("Arial", 12, "bold"),
               bg="#4CAF50", fg="white", padx=20, pady=8,
               cursor="hand2", command=change_password).pack(pady=(10, 5))
        Frame(card, bg="white", height=1).pack(fill=X, padx=30, pady=(15, 0))

        Button(card, text="🚪  Sign Out", font=("Arial", 13, "bold"),
               bg="#a6093d", fg="white", padx=20, pady=10,
               cursor="hand2", command=controller.sign_out).pack(pady=(20, 35))