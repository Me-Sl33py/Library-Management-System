from tkinter import *
from time import strftime


def hover_color(widget, normal_bg, hover_bg):
    widget.config(bg=normal_bg)
    widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
    widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))


def header_part(root, username="Guest", on_profile_click=None):
    """
    header_part now accepts:
      username         — shown in greeting (passed from each page)
      on_profile_click — function to call when profile button is clicked
    """
    header = Frame(root, bg="#a6093d", height=170)
    header.pack(fill="x")
    header.pack_propagate(False)

    #   Logo                              
    logo_frame = Frame(header, bg="#a6093d", width=200)
    logo_frame.pack(side=LEFT, padx=50, fill="y")

    logo_image = PhotoImage(file="logo.png")
    small_logo = logo_image.subsample(5, 5)

    logo_label = Label(logo_frame, image=small_logo, bg="#a6093d")
    logo_label.image = small_logo
    logo_label.pack()

    Label(
        logo_frame,
        text="Library\nManagement",
        font=("Arial", 12),
        bg="#a6093d",
        fg="white",
    ).pack()

    #   Profile + Greeting                       
    profile_frame = Frame(header, bg="#a6093d", width=300)
    profile_frame.pack(side=RIGHT, padx=20, fill="y")

    profile_image = PhotoImage(file="profile.png")
    small_profile = profile_image.subsample(5, 5)

    profile_btn = Button(
        profile_frame,
        image=small_profile,
        bg="#a6093d",
        bd=0,
        highlightthickness=0,
        cursor="hand2",
        command=on_profile_click if on_profile_click else lambda: None,
    )
    profile_btn.image = small_profile
    profile_btn.pack(side=RIGHT, padx=20)
    hover_color(profile_btn, "#a6093d", "#4fe4ee")

    #Greeting label 
    greetings_label = Label(
        profile_frame,
        font=("Arial", 16),
        fg="white",
        bg="#a6093d",
    )
    greetings_label.pack(side=LEFT)

    greetings = ["Namaste", "Konnichiwa", "Hello", "Bonjour", "Hola"]
    i = 0

    def rotate():
        nonlocal i
        # ✅ Shows the actual username in the greeting
        greetings_label.config(text=f"{greetings[i % len(greetings)]},\n{username}!")
        i += 1
        root.after(2000, rotate)

    rotate()

    return header


def body_part(root):
    body_frame = Frame(root, bg="#0d1b4c")
    body_frame.pack(fill="both", expand=True)
    return body_frame