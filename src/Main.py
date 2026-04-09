import tkinter as tk
from tkinter import font
from .mavsdkManager import MAVSDKManager
from .FlightPlanner import FlightPlanner

from src.panels.TopContainer import TopContainer
from src.panels.leftPanel import LeftPanel
from src.panels.rightPanel import RightPanel
from src.panels.bottomPanel import BottomPanel
from src.MissionController import MissionController
from src.panels.StatusBar import StatusBar


def main():
    # 'root' is the main window
    root = tk.Tk()
    root.title("GUI")
    root.geometry("600x500")
    root.rowconfigure(0, weight=0)  # status bar row — fixed
    root.rowconfigure(1, weight=1)  # top container row — expands
    root.rowconfigure(2, weight=0)  # bottom panel row — fixed
    root.columnconfigure(0, weight=1)

    # Menu Bar
    menu_font = font.Font(family='Segoe UI', size=16)
    menu = tk.Menu(root, font=menu_font)
    root.config(menu=menu)


    # Create FlightPlanner instance
    flight_planner = FlightPlanner(root)

    # Page callbacks need access to `content` and `menu`, so define them here
    def show_home():
        """Display the home page with all panels."""
        for widget in content.winfo_children():
            widget.destroy()
        
        # Recreate the home page layout
        top_frame = TopContainer.create_top_container(content)
        _left = leftPanel.create_left_panel(top_frame)
        _right = rightPanel.create_right_panel(top_frame)
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

    mavsdk = MAVSDKManager()
    mavsdk.start()

    status_bar = StatusBar()
    _status = status_bar.create_status_bar(root)
    _status.grid(row=0, column=0, sticky='ew')

    bottom_panel = BottomPanel()
    _bottom = bottom_panel.create_bottom_panel(root)
    _bottom.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

    top_container = TopContainer()
    top_frame = top_container.create_top_container(root)
    top_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=0)

    # Keep references to the panels in case we need to update them later.
    # Prefix with underscore to indicate they are intentionally unused for now

    left_panel = LeftPanel()
    _left = left_panel.create_left_panel(top_frame)

    right_panel = RightPanel()
    _right, drone_marker = right_panel.create_right_panel(top_frame)

    # Create MissionController
    mission_controller = MissionController(
        map_widget=right_panel.map_widget,
        mavsdk_manager=mavsdk
    )

    # Inject callbacks into UI
    right_panel.set_upload_callback(mission_controller.upload_mission)
    right_panel.set_start_callback(mission_controller.start_mission)
    right_panel.set_map_click_callback(mission_controller.add_waypoint)



    def refresh():
        status_bar.update_status(mavsdk.telemetry) 
        bottom_panel.update_telemetry(mavsdk.telemetry)
        right_panel.update_drone_marker(mavsdk.telemetry, drone_marker)
        root.after(200, refresh)

    refresh()

    # start the app
    root.mainloop()

if __name__ == '__main__':
    main()