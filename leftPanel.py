import tkinter as tk
from tkinter import font

def create_left_panel(parent):
    """Create and pack the left (Commands) panel inside the given parent (top_frame).

    Args:
        parent: the container (typically top_frame) to attach the left panel to.

    Returns:
        tk.Frame: the created left panel frame.
    """
    left_panel = tk.Frame(
        parent,
        bg='lightblue',
        width=100,
        height=230
    )
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)

    # Add a visible label at the top of the left panel for commands
    left_label = tk.Label(left_panel, text="COMMANDS", font=("Segoe UI", 14, 'bold'), fg='black', bg='lightblue')
    # left_label.pack(side=tk.TOP, anchor='n', pady=(8, 4))
    left_label.grid(row=0, column=0, pady=(8, 4), sticky='n')

    label_font = font.Font(family='Segoe UI', size=14, weight='bold')

    label1 = tk.Label(left_panel, text='Autonomous/Manual', font=label_font, bg='lightblue', fg='black').grid(row=1, column=0, padx=20, pady=5, sticky='nsew')
    label2 = tk.Label(left_panel, text='Return Home', font=label_font, bg='lightblue', fg='black').grid(row=2, column=0, padx=20, pady=5, sticky='nsew')
    label3 = tk.Label(left_panel, text='Hover', font=label_font, bg='lightblue', fg='black').grid(row=3, column=0, padx=20, pady=5, sticky='nsew')

    for i in range(4): 
        tk.Grid.rowconfigure(left_panel, i, weight = 1)
        tk.Grid.columnconfigure(left_panel, 0, weight = 1)

    return left_panel

