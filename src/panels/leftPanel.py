import tkinter as tk
from tkinter import font
import customtkinter as ctk

class LeftPanel:

    # Adding functionality to show which mode is currently active.
    def __init__(self, drone):
        self.drone = drone
        self.current_mode = None
        self.auto_btn = None
        self.manual_btn = None

    # The following function changes drone to 'takeoff' mode when the button
    # is clicked.
    def takeoff(self):
        print("Takeoff pressed")
        self.drone.arm_and_takeoff()

    # For 'set_autonomous_mode' and 'set_manual_mode', when that respective
    # is hit, the other button (either 'manual' or 'autonomous') is changed
    # to a white background.

    # The following function changes the drone to 'autonomous' mode when the
    # button is clicked and updates the button's appearance (green).
    def set_autonomous_mode(self):
        self.current_mode = 'autonomous'
        self.auto_btn.config(
            relief=tk.SUNKEN,
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white'
        )
        self.manual_btn.config(
            relief=tk.RAISED,
            bg=self.auto_btn.master.cget('bg'),
            fg='black',
            activebackground='#d9d9d9',
            activeforeground='black'
        )
        print("Mode set to: Autonomous")

    # The following function changes drone to 'manual' mode when the button
    # is clicked and updates the button's appearance (blue).
    def set_manual_mode(self):
        self.current_mode = 'manual'
        self.auto_btn.config(
            relief=tk.RAISED,
            bg=self.manual_btn.master.cget('bg'),
            fg='black',
            activebackground='#d9d9d9',
            activeforeground='black'
        )
        self.manual_btn.config(
            relief=tk.SUNKEN,
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white'
        )
        print("Mode set to: Manual")

    # Printing 'Returning home.'
    def return_home(self):
        print("Returning home.")
        self.drone.return_to_launch()
    
    # Printing 'Hovering at current coordinates.'
    def hover(self):
        print("Hovering at current coordinates.")
        self.drone.hover()


    def create_left_panel(self, parent):
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
        left_label = tk.Label(
            left_panel, 
            text="COMMANDS", 
            font=("Segoe UI", 14, 'bold'), 
            fg='black', 
            bg='lightblue'
        )

        left_label.grid(row=0, column=0, pady=(8, 4), sticky='n')
        label_font = font.Font(family='Segoe UI', size=14, weight='bold')
        button_font = font.Font(family='Segoe UI', size=10)

        self.auto_btn = tk.Button(
            left_panel,
            text="Autonomous",
            font=button_font,
            width=12,
            command=self.set_autonomous_mode,
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            relief=tk.RAISED
        )

        self.auto_btn.grid(row=2, column=0, pady=3)

        self.manual_btn = tk.Button(
            left_panel, 
            text="Manual",
            font=button_font,
            width=12,
            command=self.set_manual_mode,
            bg=left_panel.cget('bg'),
            fg='black',
            activebackground='#d9d9d9',
            activeforeground='black',
            relief=tk.RAISED
        )

        self.manual_btn.grid(row=3, column=0, pady=3)

        return_home_btn = tk.Button(
            left_panel, 
            text="Return Home",
            font=button_font,
            width=12,
            command=self.return_home,
            # corner_radius = 15,
            bg="#4c00ff",
            fg='white',
            relief=tk.RAISED
        )
        return_home_btn.grid(row=5, column=0, pady=3)

        hover_btn = tk.Button(
            left_panel, 
            text="Hover",
            font=button_font,
            width=12,
            command=self.hover,
            # corner_radius = 15,
            relief=tk.RAISED
        )
        hover_btn.grid(row=7, column=0, pady=3)

        takeoff_btn = tk.Button(
            left_panel,
            text="Takeoff",
            font=button_font,
            width=12,
            command=self.takeoff,
            relief=tk.RAISED
        )
        takeoff_btn.grid(row=9, column=0, pady=3)


        for i in range(8): 
            tk.Grid.rowconfigure(left_panel, i, weight = 1)
            tk.Grid.columnconfigure(left_panel, 0, weight = 1)

        return left_panel
