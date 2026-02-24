from tkinter import *
from function_header_body import *
root = Tk()
root.title('Library Management System')
root.iconbitmap('logo_icon.ico')
root.geometry('1220x880') 

header_part(root)
body_part(root)

# fist = Label(body_part(root), text='hii')
# tbel = Label(body_part, text= 'hell0',font=("Arial", 16), fg="black")
# tbel.pack()
root,mainloop()