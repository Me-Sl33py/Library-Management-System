# from tkinter import *
# from function_header_body import header_part
# from function_header_body import body_part
# from time import *
# root = Tk()
# root.title('Library Management System')
# root.iconbitmap('logo_icon.ico')
# root.geometry('1220x880')
  
# header = header_part(root)
# body = body_part(root)



# root.mainloop()

from database_operations import *

add_book("yourname", "hehe", 2023, 5)
print(get_all_books())