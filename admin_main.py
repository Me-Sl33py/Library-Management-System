from tkinter import *
import tkinter.messagebox as messagebox

from home_page        import HomePage
from add_update       import AddUpdatePage
from delete_books     import DeleteBooksPage
from available_books  import AvailableBooksPage
from registered_user  import RegisteredUserPage
from records          import RecordsPage
from history          import HistoryPage
from profile_page     import ProfilePage


class AdminMain(Tk):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.title("Library Management — Admin")
        self.geometry("1220x900")
        self.state("zoomed")
        self.iconbitmap("logo_icon.ico")
        self.resizable(True, True)

        container = Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        pages = [
            ("HomePage",           HomePage,           {}),
            ("AddUpdatePage",      AddUpdatePage,      {}),
            ("DeleteBooksPage",    DeleteBooksPage,    {}),
            ("AvailableBooksPage", AvailableBooksPage, {}),
            ("RegisteredUserPage", RegisteredUserPage, {}),
            ("RecordsPage",        RecordsPage,        {}),
            ("HistoryPage",        HistoryPage,        {}),
            ("ProfilePage",        ProfilePage,        {}),
        ]
        for name, PageClass, kwargs in pages:
            frame = PageClass(container, self, username=username, **kwargs)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, name):
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

    def sign_out(self):
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            self.destroy()
            import library_login
            library_login.run()


if __name__ == "__main__":
    app = AdminMain("Manish")
    app.mainloop()