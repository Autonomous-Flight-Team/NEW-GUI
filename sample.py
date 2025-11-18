# To run this code, use: 'python sample.py'

import tkinter as tk
from tkinter import *
import tkintermapview

# Need to include this import to use fonts as the above 'from tkinter...' statement
# only imports from tkinter, but not its submodules (which includes fonts).
from tkinter import font

# 'root' is the main window
root = Tk()
root.title("Sample Tkinter Window")
root.geometry("600x500")



# START Menu Bar Code

# The following is creating a Menu Bar

# Increasing the size of the menu bar not working... need to fix.
menu_font = font.Font(family='Segoe UI', size=10)

menu = Menu(root, font=menu_font)
# menu.place(x=0, y=0, width=600, height=20)

# 'root.config(menu=menu)' line links the menu bar to the main window.
root.config(menu=menu)

content = Frame(root)
# content.pack(fill=BOTH, expand=True)

Label(content, text="Welcome to the GUI for the Autonomous Flight Team!",
      font=("Segoe UI", 16)).pack(pady=50)

# Page for the Quadcopter
def show_quadcopter():
    for widget in content.winfo_children():
        widget.destroy()
    # Label(content, text="Quadcopter Page", font=("Segoe UI", 14)).pack(pady=5)

# Page for the Fixed Wing
def show_fixed_wing():
    for widget in content.winfo_children():
        widget.destroy()
    # Label(content, text="Fixed Wing Page", font=("Segoe UI", 14)).pack(pady=5)

# Home Page
def show_home():
    for widget in content.winfo_children():
        widget.destroy()
    # Label(content, text="Welcome to the GUI for the Autonomous Flight Team!",
    #       font=("Segoe UI", 16)).pack(pady=5)

flightmodes = Menu(menu)
menu.add_cascade(label='PICO Menu', menu=flightmodes)
# menu.add_command(label='Home', command=show_home)
flightmodes.add_command(label='Quadcopter', command=show_quadcopter)
flightmodes.add_command(label='Fixed Wing', command=show_fixed_wing)
flightmodes.add_command(label='Home', command=show_home)

# END Menu Bar code

# START Home Page Panels Code

# =================================================
# Top Container - holds the left and right panels.
# =================================================

# Creating a container frame to hold the top two panels. 
# Creating this frame allows us to align the left/right panels in an easier way.
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # side=tk.TOP -> places this container at the top of the window
    # fill=tk.BOTH -> allows the container to stretch horizontally & vertically 
    # expand=True -> allows frame to grow/shrink if window is resized

# ------------------------
# Left Panel (Commands)
# ------------------------
left_panel = tk.Frame(
    top_frame,          # parent is 'top_frame'
    bg='lightblue',     # background color
    width=100,          # default width when window is first opened (Tkinter may resize)
    height=230          # default height
)
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
    # side=tk.LEFT -> places this panel on the left side of 'top_frame'
    # fill=tk.BOTH -> allows the panel to stretch horizontally & vertically
    # expand=True -> allows panel to grow/shrink if window is resized
    # padx/pady=10 -> adds padding (extra space with bckg color) around the frame

# Add a visible label at the top of the left panel for commands
left_label = tk.Label(left_panel, text="Commands", font=("Segoe UI", 14, 'bold'), fg='black', bg='lightblue')
left_label.pack(side=tk.TOP, anchor='n', pady=(8,4))

# ------------------------
# Right Panel (MAP)
# ------------------------
right_panel = tk.Frame(
    top_frame, 
    bg='lightgreen', 
    width=360, 
    height=230
)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=10)
    # side=tk.RIGHT -> places this panel on the right side of 'top_frame'

# Add a visible label at the top of the right panel for the map
right_label = tk.Label(right_panel, text="MAP", font=("Segoe UI", 14, 'bold'), fg='black', bg='lightgreen')
right_label.pack(side=tk.TOP, anchor='n', pady=(8,4))

# create map widget
map_widget = tkintermapview.TkinterMapView(right_panel, width=360, height=230, corner_radius=0)
map_widget.pack(fill=tk.BOTH, expand=True)
# set current widget position and zoom
map_widget.set_position(47.65821445872502, -122.30391059662294)  # McMahon
map_widget.set_zoom(15)

# ========================================
# Bottom Panel (Data - Altitude, etc.)
# ========================================
bottom_panel = tk.Frame(
    root, 
    bg='lightgrey', 
    width=540, 
    height=150
)
bottom_panel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Add a visible label at the top of the bottom panel for telemetry/data
bottom_label = tk.Label(bottom_panel, text="DATA - Altitude, Speed, Heading", font=("Segoe UI", 13, 'bold'), fg='black', bg='lightgrey')
bottom_label.pack(side=tk.TOP, anchor='n', pady=(6,4))

# END Home Page Panels Code

root.mainloop()