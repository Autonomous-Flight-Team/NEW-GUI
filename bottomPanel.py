import tkinter as tk
from tkinter import font

def create_bottom_panel(parent):
    """Create and pack the bottom data panel inside the given parent (typically root).

    Args:
        parent: the container (usually the main root) to attach the bottom panel to.

    Returns:
        tk.Frame: the created bottom panel frame.
    """
    bottom_panel = tk.Frame(
        parent,
        bg='lightgrey',
        width=540,
        height=150
    )
    bottom_panel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Add a visible label at the top of the bottom panel for telemetry/data
    data_title = tk.Label(bottom_panel, text="TELEMETRY DATA", font=("Segoe UI", 16, 'bold'), fg='black', bg='lightgrey')
    data_title.pack(side=tk.TOP, anchor='n', pady=(6, 4))

    labels = tk.Frame(bottom_panel, bg='lightgrey')
    labels.pack(anchor='center', fill=tk.BOTH, expand=True)

    label_font = font.Font(family='Segoe UI', size=14, weight='bold')
    label1 = tk.Label(labels, text='Altitude', font=label_font, bg='lightgrey', fg='black').grid(row=0, column=0, padx=20, pady=5, sticky='nsew')
    # display data in row=0, column=1

    label2 = tk.Label(labels, text='Ground Speed', font=label_font, bg='lightgrey', fg='black').grid(row=0, column=2, padx=20, pady=5, sticky='nsew')
    # display data in row=0, column=3

    label3 = tk.Label(labels, text='Yaw', font=label_font, bg='lightgrey', fg='black').grid(row=1, column=0, padx=20, pady=5, sticky='nsew')
    label4 = tk.Label(labels, text='Vertical Velocity', font=label_font, bg='lightgrey', fg='black').grid(row=1, column=2, padx=20, pady=5, sticky='nsew')
    label5 = tk.Label(labels, text='Distance to WP', font=label_font, bg='lightgrey', fg='black').grid(row=2, column=0, padx=20, pady=5, sticky='nsew')
    label6 = tk.Label(labels, text='Distance from home', font=label_font, bg='lightgrey', fg='black').grid(row=2, column=2, padx=20, pady=5, sticky='nsew')

    for i in range(3): 
        tk.Grid.rowconfigure(labels, i, weight = 1)
        tk.Grid.columnconfigure(labels, i, weight = 1)


    return bottom_panel