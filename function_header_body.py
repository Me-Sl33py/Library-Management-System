from tkinter import *
from time import *
# root = Tk()
# root.title('Library Management System')
# root.iconbitmap('logo_icon.ico')
# root.geometry('1220x880')
def header_part(root):
    
    header = Frame(root, bg="#a6093d",  height=170)
    header.pack(pady=0, fill='x')
    header.pack_propagate(False)

    logo_frame = Frame(header, bg="#a6093d",width=200, height=150)
    logo_frame.pack(side=LEFT, padx=50)
    logo_frame.pack_propagate(False)

    logo_image = PhotoImage(file='logo.png')
    small_logo_image = logo_image.subsample(5,5)
    
    logo_label = Label(logo_frame, image=small_logo_image, bg="#a6093d")
    logo_label.image = small_logo_image
    logo_label.pack(side= 'top', padx=10)

    below_logo = Label(logo_frame, text="Library\n Management",font=("Arial", 12), bg='#a6093d', fg='white')
    below_logo.pack(side='bottom')

    profile_frame = Frame(header, bg="#a6093d",width=300, height=150)
    profile_frame.pack(side=RIGHT, padx=10)
    profile_frame.pack_propagate(False)

    profile_image = PhotoImage(file='profile.png')
    small_profile_image = profile_image.subsample(5,5)
    
    profile_label = Label(profile_frame, image=small_profile_image, bg="#a6093d")
    profile_label.image = small_profile_image
    profile_label.pack(side= 'right', padx=30)

    greetings = [
        "Namaste",        # Nepal
        "Konnichiwa",     # Japan
        "Hello",          # English
        "Bonjour",        # French
        "Hola",           # Spanish
        "Hallo",          # German
        "Ciao",           # Italian
        "Nǐ hǎo",         # Chinese (Mandarin)
        "Annyeong",       # Korean
        "Salam",          # Arabic / Persian
        "Olá",            # Portuguese
        "Sawasdee",       # Thai
        "Hej",            # Swedish
        "Hei",            # Finnish
        "Merhaba"         # Turkish
    ]

    greetings_label = Label(profile_frame, text="", font=("Arial", 16), fg="black", bg='#a6093d')
    greetings_label.pack(side=LEFT, padx=1)

    i = 0
    def rotate_greetings():
        nonlocal i
        greetings_label.config(text=f"{greetings[i% len(greetings)]}\n Welcome!")
        i += 1
        root.after(2000, rotate_greetings)

    rotate_greetings()
    return header

def body_part(root):
    body_frame = Frame(root, bg="#0d1b4c")
    body_frame.pack(fill='both', expand=True)
    body_frame.pack_propagate(False)

    time_label = Label(body_frame, font=("Arial", 16), fg="black")
    time_label.pack(side='bottom', anchor= 'e', padx=30, pady=30)


    def update_time():
        current = strftime("%d-%m-%Y \n%H:%M:%S")
        time_label.config(text=current)
        root.after(1000, update_time)

    update_time()
    return body_frame
# header = header_part(root)
# body = body_part(root)
# root.mainloop()