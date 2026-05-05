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
from src.panels.leftPanel import LeftPanel


def main():
    # 'root' is the main window
    root = tk.Tk()
    root.title("GUI")
    root.geometry("700x550")
    root.rowconfigure(0, weight=0)  # status bar row — fixed
    root.rowconfigure(1, weight=1)  # top container row — expands
    root.rowconfigure(2, weight=1)  # bottom panel row — fixed
    root.columnconfigure(0, weight=1)

    # Menu Bar
    menu_font = font.Font(family='Segoe UI', size=16)
    menu = tk.Menu(root, font=menu_font)
    root.config(menu=menu)


    # Create FlightPlanner instance
    flight_planner = FlightPlanner(root)

    # Create a content frame that holds the current page.
    content = tk.Frame(root, bg='white')
    content.grid(row=1, column=0, sticky='nsew', padx=5, pady=0)

    # Track the current map marker so refresh only updates it when visible.
    drone_marker = None

    def show_home():
        """Display the home page with all panels."""
        nonlocal drone_marker
        for widget in content.winfo_children():
            widget.destroy()

        top_container = TopContainer()
        top_frame = top_container.create_top_container(content)
        top_frame.pack(fill=tk.BOTH, expand=True)

        _left = left_panel.create_left_panel(top_frame)
        _, drone_marker = right_panel.create_right_panel(top_frame)

    def show_flight_planner():
        """Display the flight planner page."""
        for widget in content.winfo_children():
            widget.destroy()
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

    left_panel = LeftPanel(mavsdk)
    right_panel = RightPanel()

    # Show the home page initially.
    show_home()

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
        if drone_marker is not None and right_panel.map_widget is not None and right_panel.map_widget.winfo_exists():
            right_panel.update_drone_marker(mavsdk.telemetry, drone_marker)
        root.after(200, refresh)

    refresh()

    # start the app
    root.mainloop()

if __name__ == '__main__':
    main()