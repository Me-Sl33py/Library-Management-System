# ui_pop.py
from tkinter import messagebox


def confirm_action(title="Confirm", message="Are you sure?"):
    """
    Generic Yes/No confirmation popup.
    Returns True if user clicks Yes, False if No.
    """
    return messagebox.askyesno(title, message)


def show_success(message="Operation successful"):
    """
    Success information popup.
    """
    messagebox.showinfo("Success", message)


def show_error(message="Something went wrong"):
    """
    Error popup.
    """
    messagebox.showerror("Error", message)


def show_warning(message="Please check your input"):
    """
    Warning popup.
    """
    messagebox.showwarning("Warning", message)

