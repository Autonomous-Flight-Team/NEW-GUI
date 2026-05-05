import tkinter as tk
from tkinter import font, messagebox, ttk
import math


class FlightPlanner:
    """Flight Planner for PICO Fixed Wing UAV."""

    def __init__(self, parent, right_panel=None):
        """Initialize the Flight Planner.

        Args:
            parent:      Parent tkinter widget (main window)
            right_panel: RightPanel instance for status logging (optional)
        """
        self.parent = parent
        self.right_panel = right_panel
        self.waypoints = []  # Store waypoints as list of (lat, lon) tuples
        self.map_widget = None
        self.waypoint_listbox = None

    def log_status(self, message: str):
        """Forward a status message to the RightPanel MAVLink log.

        Falls back to stdout if no RightPanel is attached.
        """
        if self.right_panel is not None:
            self.right_panel.log_status(message)
        else:
            print(message)