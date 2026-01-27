import tkinter as tk
from tkinter import font

class BottomPanel: 
    def __init__(self):
        self.live_labels = {}

    def create_bottom_panel(self, parent):
        """Create and pack the bottom data panel inside the given parent (typically root).

        Args:
            parent: the container (usually the main root) to attach the bottom panel to.

        Returns:
            tk.Frame: the created bottom panel frame.
        """
        self.root = parent

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

        def make_label(key, text, row, col):
            lbl = tk.Label(labels, text=text, font=label_font, bg='lightgrey', fg='black')
            lbl.grid(row=row, column=col, padx=20, pady=5, sticky='nsew')
            self.live_labels[key] = lbl

        make_label("altitude", "Altitude", 0, 0)
        make_label("ground_speed", "Ground Speed", 0, 1)
        make_label("yaw", "Yaw", 1, 0)
        make_label("vertical_speed", "Vertical Velocity", 1, 1)
        make_label("distance_to_wp", "Distance to WP", 2, 0)
        make_label("distance_from_home", "Distance from Home", 2, 1)

        for i in range(2): 
            tk.Grid.rowconfigure(labels, i, weight = 1)
            tk.Grid.columnconfigure(labels, i, weight = 1)

        return bottom_panel
    
    def update_telemetry(self, telemetry):
        def update(val):
            if val is None:
                return "---"
            else:
                return str(val)

        self.live_labels["altitude"].config(text=f"Altitude: {update(telemetry['altitude'])}")
        self.live_labels["ground_speed"].config(text=f"Ground Speed: {update(telemetry['ground_speed'])}")
        self.live_labels["yaw"].config(text=f"Yaw: {update(telemetry['yaw'])}")
        self.live_labels["vertical_speed"].config(text=f"Vertical Speed: {update(telemetry['vertical_speed'])}")