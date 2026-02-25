from tkinter import *
from function_header_body import header_part, body_part, hover_color
root = Tk()
root.title('Library Management System')
root.iconbitmap('logo_icon.ico')
root.geometry('1220x1200') 
# root.resizable(0,0)    

header = header_part(root)
body = body_part(root)

row1 = Frame(body, bg="#0d1b4c", height=250)
row1.pack(pady=10, fill= "x", padx=240, anchor='center')
row1.pack_propagate(False)

row2 = Frame(body, bg="#0d1b4c", height=250)
row2.pack(pady=10, fill= "x", padx=240, anchor='center')
row2.pack_propagate(False)

add_update_btn = Button(row1, text="Add or Update \nBook",
             bg="white",      
             fg="black",
             font=("Arial", 16, "bold"),
             width=16,
             height=4,
             relief="flat",     
             bd=0)  
add_update_btn.pack(side=LEFT, expand=True, fill='x', padx=10)
hover_color(add_update_btn, "white", "aqua")

delete_book_btn = Button(row1, text="Delete Books",
             bg="white",      
             fg="black",
             font=("Arial", 16, "bold"),
             width=16,
             height=4,
             relief="flat",     
             bd=0)  
delete_book_btn.pack(side=LEFT, expand=True, fill='x', padx=10)
hover_color(delete_book_btn, "white", "aqua")

avaliable_books_btn = Button(row1, text="Avaliable\n Books",
             bg="white",      
             fg="black",
             font=("Arial", 16, "bold"),
             width=16,
             height=4,
             relief="flat",     
             bd=0)  
avaliable_books_btn.pack(side=LEFT, expand=True, fill='x', padx=10)
hover_color(avaliable_books_btn, "white", "aqua")

registered_user_btn = Button(row2, text="Register Users",
             bg="white",      
             fg="black",
             font=("Arial", 16, "bold"),
             width=16,
             height=4,
             relief="flat",     
             bd=0)  
registered_user_btn.pack(side=LEFT, expand=True, fill='x', padx=10)
hover_color(registered_user_btn, "white", "aqua")

history_btn = Button(row2, text="History",
             bg="white",      
             fg="black",
             font=("Arial", 16, "bold"),
             width=16,
             height=4,
             relief="flat",     
             bd=0)  
history_btn.pack(side=LEFT, expand=True, fill='x', padx=10)
hover_color(history_btn, "white", "aqua")

records_btn = Button(row2, text="Records",
             bg="white",      
             fg="black",
             font=("Arial", 16, "bold"),
             width=16,
             height=4,
             relief="flat",     
             bd=0)  
records_btn.pack(side=LEFT, expand=True, fill='x', padx=10)
hover_color(records_btn, "white", "aqua")
root.mainloop()