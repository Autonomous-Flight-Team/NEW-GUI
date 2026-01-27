import tkinter as tk
from tkinter import font, messagebox, ttk
import math


class FlightPlanner:
    """Flight Planner for PICO Fixed Wing UAV."""
    
    def __init__(self, parent):
        """Initialize the Flight Planner.
        
        Args:
            parent: Parent tkinter widget (main window)
        """
        self.parent = parent
        self.waypoints = []  # Store waypoints as list of (lat, lon) tuples
        self.map_widget = None
        self.waypoint_listbox = None
    
    def create_flight_planner_page(self, content_frame):
        """Create and display the flight planner page.
        
        Args:
            content_frame: The container frame to fill with flight planner UI
        """
        # Clear existing content
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        # Add a title
        title_label = tk.Label(
            content_frame,
            text="Flight Planner - PICO Fixed Wing",
            font=("Segoe UI", 16, 'bold'),
            bg='white',
            fg='#1f77b4'
        )
        title_label.pack(pady=(10, 10))
        
        # Placeholder for now
        placeholder = tk.Label(
            content_frame,
            text="Flight Planner interface coming soon...",
            font=("Segoe UI", 12)
        )
        placeholder.pack(pady=20)
