# To run this code, use: 'python sample.py'

import tkinter as tk
from tkinter import font

import TopContainer
import leftPanel
import rightPanel
import bottomPanel


def main():
    # 'root' is the main window
    root = tk.Tk()
    root.title("Sample Tkinter Window")
    root.geometry("600x500")

    # START Menu Bar Code
    menu_font = font.Font(family='Segoe UI', size=56)
    menu = tk.Menu(root, font=menu_font)
    root.config(menu=menu)

    content = tk.Frame(root)
    tk.Label(content, text="Welcome to the GUI for the Autonomous Flight Team!",
             font=("Segoe UI", 16)).pack(pady=50)

    # Page callbacks need access to `content` and `menu`, so define them here
    def show_quadcopter():
        for widget in content.winfo_children():
            widget.destroy()
        tk.Label(content, text="Quadcopter Page", font=("Segoe UI", 14)).pack(pady=5)

    def show_fixed_wing():
        for widget in content.winfo_children():
            widget.destroy()
        tk.Label(content, text="Fixed Wing Page", font=("Segoe UI", 14)).pack(pady=5)

    def show_home():
        for widget in content.winfo_children():
            widget.destroy()
        tk.Label(content, text="Welcome to the GUI for the Autonomous Flight Team!",
                 font=("Segoe UI", 16)).pack(pady=50)

    # Menu items
    flightmodes = tk.Menu(menu)
    menu.add_cascade(label='PICO Menu', menu=flightmodes)
    menu.add_command(label='Home', command=show_home)
    flightmodes.add_command(label='Quadcopter', command=show_quadcopter)
    flightmodes.add_command(label='Fixed Wing', command=show_fixed_wing)

    # Create containers/panels using the modularized functions
    top_frame = TopContainer.create_top_container(root)
    # Keep references to the panels in case we need to update them later.
    # Prefix with underscore to indicate they are intentionally unused for now
    _left = leftPanel.create_left_panel(top_frame)
    _right = rightPanel.create_right_panel(top_frame)
    _bottom = bottomPanel.create_bottom_panel(root)

    # start the app
    root.mainloop()


if __name__ == '__main__':
    main()





