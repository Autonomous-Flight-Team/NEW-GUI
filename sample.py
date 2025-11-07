# To run this code, use: 'python sample.py'

import tkinter as tk
from tkinter import *

# Need to include this import to use fonts as the above 'from tkinter...' statement
# only imports from tkinter, but not its submodules (which includes fonts).
from tkinter import font

# m = tk.Tk()
# m.title("Sample Tkinter Window")
# m.geometry("400x300")
# m.mainloop()

# 'root' is the main window
root = Tk()
root.title("Sample Tkinter Window")
root.geometry("600x500")
w = Label(root, text="Hello World!")
w = Label(root)
w.pack()

# The following is creating a Menu Bar

# Increasing the size of the menu bar not working... need to fix.
menu_font = font.Font(family='Segoe UI', size=56)

menu = Menu(root, font=menu_font)
# menu.place(x=0, y=0, width=600, height=20)

# 'root.config(menu=menu)' line links the menu bar to the main window.
root.config(menu=menu)

content = Frame(root)
content.pack(fill=BOTH, expand=True)

Label(content, text="Welcome to the GUI for the Autonomous Flight Team!",
      font=("Segoe UI", 16)).pack(pady=50)

# Page for the Quadcopter
def show_quadcopter():
    for widget in content.winfo_children():
        widget.destroy()
    Label(content, text="Quadcopter Page", font=("Segoe UI", 14)).pack(pady=50)

# Page for the Fixed Wing
def show_fixed_wing():
    for widget in content.winfo_children():
        widget.destroy()
    Label(content, text="Fixed Wing Page", font=("Segoe UI", 14)).pack(pady=50)

# Home Page
def show_home():
    for widget in content.winfo_children():
        widget.destroy()
    Label(content, text="Welcome to the GUI for the Autonomous Flight Team!",
          font=("Segoe UI", 16)).pack(pady=50)

flightmodes = Menu(menu)
menu.add_cascade(label='PICO Menu', menu=flightmodes)
menu.add_command(label='Home', command=show_home)
flightmodes.add_command(label='Quadcopter', command=show_quadcopter)
flightmodes.add_command(label='Fixed Wing', command=show_fixed_wing)
flightmodes.add_command(label='Home', command=show_home)

# End Menu Bar code

root.mainloop()





