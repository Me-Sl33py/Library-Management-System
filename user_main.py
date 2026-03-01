from tkinter import *
import tkinter.messagebox as messagebox

from user_home_page      import UserHomePage
from available_books     import AvailableBooksPage
from user_pending_books  import UserPendingBooksPage
from user_history        import UserHistoryPage
from user_renew_book     import UserRenewBookPage
from profile_page        import ProfilePage


class UserProfilePage(ProfilePage):
    """Profile page for user portal — back button goes to UserHomePage."""
    def __init__(self, parent, controller, username="Guest"):
        super().__init__(parent, controller, username)
        # Override the header profile-click to go to UserHomePage
        # (ProfilePage already works; just the sign_out destination is the same)


class UserMain(Tk):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.title("Library Management — User Portal")
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
            ("UserHomePage",           UserHomePage,                        {}),
            ("UserAvailableBooksPage", AvailableBooksPage,                  {"back_dest":"UserHomePage"}),
            ("UserPendingBooksPage",   UserPendingBooksPage,                {}),
            ("UserHistoryPage",        UserHistoryPage,                     {}),
            ("UserRenewBookPage",      UserRenewBookPage,                   {}),
            ("UserProfilePage",        UserProfilePage,                     {}),
        ]
        for name, PageClass, kwargs in pages:
            frame = PageClass(container, self, username=username, **kwargs)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("UserHomePage")

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
    app = UserMain("Hilson")
    app.mainloop()