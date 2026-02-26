from tkinter import *
from function_header_body import header_part, body_part, hover_color

root = Tk()
root.title("Library Management System")
root.geometry("1220x900")
root.iconbitmap("logo_icon.ico")

header = header_part(root)
body = body_part(root)

# Main _container
container = Frame(body, bg="#0d1b4c", width=1100, height=600)
container.place(relx=0.5, rely=0.5, anchor=CENTER)
container.pack_propagate(False)

#manage_grid
for i in range(3):
    container.columnconfigure(i, weight=1, uniform="col")
for i in range(2):
    container.rowconfigure(i, weight=1, uniform="row")

# Button_names
buttons = [
    {"text": "Add or Update\n Book", "icon": "📖", "color": "#4CAF50"},
    {"text": "Delete Books", "icon": "🗑️", "color": "#f44336"},
    {"text": "Available Books", "icon": "📚", "color": "#2196F3"},
    {"text": "Register Users", "icon": "👤", "color": "#FF9800"},
    {"text": "History", "icon": "📋", "color": "#9C27B0"},
    {"text": "Records", "icon": "📊", "color": "#009688"},
]

for index, btn_info in enumerate(buttons):
    r = index // 3
    c = index % 3

    #frame_button
    btn_frame = Frame(container, bg="white")
    btn_frame.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
    
    # Icon_label
    icon_label = Label(btn_frame, text=btn_info["icon"], font=("Arial", 40), 
                       bg="white", fg=btn_info["color"])
    icon_label.pack(pady=(20, 10))
    
    #Button_text
    text_label = Label(btn_frame, text=btn_info["text"], 
                       font=("Arial", 14, "bold"), bg="white", fg="black")
    text_label.pack(pady=(0, 20))
    
    # Make the entire frame clickable
    def make_command(text=btn_info["text"]):
        def command():
            print(f"Clicked: {text}")
        return command
    
    # Bind click events to the entire frame
    btn_frame.bind("<Button-1>", lambda e, t=btn_info["text"]: print(f"Clicked: {t}"))
    icon_label.bind("<Button-1>", lambda e, t=btn_info["text"]: print(f"Clicked: {t}"))
    text_label.bind("<Button-1>", lambda e, t=btn_info["text"]: print(f"Clicked: {t}"))
    
    # Add hover effect to entire frame
    def on_enter(e, frame=btn_frame, icon=icon_label, text=text_label):
        frame.config(bg="aqua")
        icon.config(bg="aqua")
        text.config(bg="aqua")
    
    def on_leave(e, frame=btn_frame, icon=icon_label, text=text_label):
        frame.config(bg="white")
        icon.config(bg="white")
        text.config(bg="white")
    
    btn_frame.bind("<Enter>", on_enter)
    btn_frame.bind("<Leave>", on_leave)
    icon_label.bind("<Enter>", on_enter)
    icon_label.bind("<Leave>", on_leave)
    text_label.bind("<Enter>", on_enter)
    text_label.bind("<Leave>", on_leave)
    
    # Configure frame to look like a button
    btn_frame.config(relief="raised", bd=2)

root.mainloop()