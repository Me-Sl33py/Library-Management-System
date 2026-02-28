# # # from tkinter import *
# # # from function_header_body import header_part
# # # from function_header_body import body_part
# # # from time import *
# # # root = Tk()
# # # root.title('Library Management System')
# # # root.iconbitmap('logo_icon.ico')
# # # root.geometry('1220x880')
  
# # # header = header_part(root)
# # # body = body_part(root)



# # # root.mainloop()

# # from database_operations import *

# # add_book("yourname", "hehe", 2023, 5)
# # print(get_all_books())

# from ui_pop import confirm_action, show_success, show_error, show_warning


# if __name__ == "__main__":
#     from tkinter import Tk
    
#     root = Tk()
#     root.withdraw()  # hides main empty window

#     if confirm_action("Test", "Do you want to continue?"):
#         show_success("You clicked YES!")
#     else:
#         show_error("You clicked NO!")
    
#     root.destroy()
      

# Sample Users with passwords
            users = [
                ('Manish', 'adminpass', 'admin'),
                ('Tshering', 'adminpass', 'admin'),
                ('Hilson', 'userpass1', 'user'),
                ('Bibek', 'userpass2', 'user')
            ]
            cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", users)