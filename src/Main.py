import tkinter as tk
from tkinter import font
from .mavsdkManager import MAVSDKManager
from .FlightPlanner import FlightPlanner

from src.panels.TopContainer import TopContainer
from src.panels.leftPanel import LeftPanel
from src.panels.rightPanel import RightPanel
from src.panels.bottomPanel import BottomPanel
from src.drone_controller import DroneController
from src.panels.leftPanel import LeftPanel


def main():
    # 'root' is the main window
    root = tk.Tk()
    root.title("GUI")
    root.geometry("600x500")

    # Menu Bar
    menu_font = font.Font(family='Segoe UI', size=16)
    menu = tk.Menu(root, font=menu_font)
    root.config(menu=menu)

    content = tk.Frame(root)
    content.pack(fill=tk.BOTH, expand=True)

    # Create FlightPlanner instance
    flight_planner = FlightPlanner(root)

    # Page callbacks need access to `content` and `menu`, so define them here
    def show_home():
        """Display the home page with all panels."""
        for widget in content.winfo_children():
            widget.destroy()
        
        # Recreate the home page layout
        top_frame = TopContainer.create_top_container(content)
        _left = left_panel.create_left_panel(top_frame)
        _right = right_panel.create_right_panel(top_frame)
        # Note: bottom_panel stays at root level, not in content

    def show_flight_planner():
        """Display the flight planner page."""
        flight_planner.create_flight_planner_page(content)

    # Menu items
    select_uav = tk.Menu(menu)
    menu.add_cascade(label='Select UAV', menu=select_uav)
    select_uav.add_command(label='Quadcopter')
    select_uav.add_command(label='Fixed Wing')
    main_menu = tk.Menu(menu)
    menu.add_cascade(label='Menu', menu=main_menu)
    main_menu.add_command(label='Home', command=show_home)
    main_menu.add_command(label='Flight Planner', command=show_flight_planner)
    main_menu.add_command(label='Telemetry Logs')

    # Create containers/panels using the modularized functions
    top_container = TopContainer()
    top_frame = top_container.create_top_container(root)

    # Keep references to the panels in case we need to update them later.
    # Prefix with underscore to indicate they are intentionally unused for now
    drone = DroneController()
    left_panel = LeftPanel(drone)
    _left = left_panel.create_left_panel(top_frame)

    right_panel = RightPanel()
    _right, drone_marker, map_widget = right_panel.create_right_panel(top_frame)

    bottom_panel = BottomPanel()
    _bottom = bottom_panel.create_bottom_panel(root)

    mavsdk = MAVSDKManager()
    mavsdk.start()

    def refresh():
        bottom_panel.update_telemetry(mavsdk.telemetry)
        right_panel.update_drone_marker(mavsdk.telemetry, drone_marker, map_widget)
        root.after(200, refresh)

    refresh()

    # start the app
    root.mainloop()

if __name__ == '__main__':
    main()