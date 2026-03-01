from tkinter import *


def hover_color(widget, normal_bg, hover_bg):
    widget.config(bg=normal_bg)
    widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
    widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))


def header_part(root, username="Guest", on_profile_click=None):
    header = Frame(root, bg="#a6093d", height=170)
    header.pack(fill="x")
    header.pack_propagate(False)

    # Logo
    logo_frame = Frame(header, bg="#a6093d", width=200)
    logo_frame.pack(side=LEFT, padx=50, fill="y")
    logo_image = PhotoImage(file="logo.png")
    small_logo = logo_image.subsample(5, 5)
    logo_label = Label(logo_frame, image=small_logo, bg="#a6093d")
    logo_label.image = small_logo
    logo_label.pack()
    Label(logo_frame, text="Library\nManagement",
          font=("Arial", 12), bg="#a6093d", fg="white").pack()

    # Profile + Greeting
    profile_frame = Frame(header, bg="#a6093d", width=300)
    profile_frame.pack(side=RIGHT, padx=20, fill="y")
    profile_image = PhotoImage(file="profile.png")
    small_profile = profile_image.subsample(5, 5)
    profile_btn = Button(profile_frame, image=small_profile,
                         bg="#a6093d", bd=0, highlightthickness=0,
                         cursor="hand2",
                         command=on_profile_click if on_profile_click else lambda: None)
    profile_btn.image = small_profile
    profile_btn.pack(side=RIGHT, padx=20)
    hover_color(profile_btn, "#a6093d", "#4fe4ee")

    greetings_label = Label(profile_frame, font=("Arial", 16), fg="white", bg="#a6093d")
    greetings_label.pack(side=LEFT)
    greetings = ["Namaste", "Konnichiwa", "Hello", "Bonjour", "Hola"]
    i = [0]

    def rotate():
        greetings_label.config(text=f"{greetings[i[0] % len(greetings)]},\n{username}!")
        i[0] += 1
        root.after(2000, rotate)
    rotate()
    return header


def body_part(root):
    body_frame = Frame(root, bg="#0d1b4c")
    body_frame.pack(fill="both", expand=True)
    return body_frame


def make_back_btn(parent, controller, dest="HomePage"):
    """Styled back button — call inside any page's content frame."""
    bf = Frame(parent, bg="#a6093d", relief="raised", bd=2)
    bf.pack(anchor="w", padx=20, pady=(15, 0))
    bi = Label(bf, text="←", font=("Arial", 16), bg="#a6093d", fg="white")
    bi.pack(side=LEFT, padx=5)
    bt = Label(bf, text="Back to Home", font=("Arial", 12), bg="#a6093d", fg="white")
    bt.pack(side=LEFT, padx=(0, 8))

    def go(e=None):   controller.show_frame(dest)
    def hl_on(e):
        for w in (bf, bi, bt): w.config(bg="#4fe4ee")
    def hl_off(e):
        for w in (bf, bi, bt): w.config(bg="#a6093d")
    for w in (bf, bi, bt):
        w.bind("<Button-1>", go)
        w.bind("<Enter>", hl_on)
        w.bind("<Leave>", hl_off)


def icon_btn(parent, label, icon, color, cmd):
    """Small icon+text button used throughout the app."""
    frm = Frame(parent, bg="white", relief="raised", bd=2)
    frm.pack(side=LEFT, padx=8)
    il = Label(frm, text=icon, font=("Arial", 18), bg="white", fg=color)
    il.pack(side=LEFT, padx=8)
    tl = Label(frm, text=label, font=("Arial", 12, "bold"), bg="white", fg="black")
    tl.pack(side=LEFT, padx=(0, 8))

    def on_e(e):
        for w in (frm, il, tl): w.config(bg="lightblue")
    def on_l(e):
        for w in (frm, il, tl): w.config(bg="white")
    for w in (frm, il, tl):
        w.bind("<Button-1>", lambda e, c=cmd: c())
        w.bind("<Enter>", on_e)
        w.bind("<Leave>", on_l)
    return frm