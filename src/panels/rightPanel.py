import tkinter as tk
import tkintermapview


class RightPanel:

    def __init__(self):
        self.map_widget = None
        self.upload_button = None
        self.start_button = None

    def create_right_panel(self, parent):
        right_panel = tk.Frame(parent, bg='lightblue')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=10)

        tk.Label(
            right_panel,
            text="MAP",
            font=("Segoe UI", 14, 'bold'),
            fg='black',
            bg='lightblue'
        ).pack(pady=(8, 4))

        # Map
        self.map_widget = tkintermapview.TkinterMapView(
            right_panel,
            corner_radius=0
        )
        self.map_widget.pack(fill=tk.BOTH, expand=True)
        self.map_widget.set_zoom(15)

        # Buttons
        button_frame = tk.Frame(right_panel, bg="lightblue")
        button_frame.pack(fill=tk.X, pady=5)

        self.upload_button = tk.Button(button_frame, text="Upload Mission")
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(button_frame, text="Start Mission")
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Drone marker placeholder
        drone_marker = self.map_widget.set_marker(
            0, 0,
            text="DRONE",
            marker_color_circle="red",
            marker_color_outside="white"
        )

        return right_panel, drone_marker

    # ------------------------
    # Public wiring methods
    # ------------------------

    def set_upload_callback(self, callback):
        self.upload_button.config(command=callback)

    def set_start_callback(self, callback):
        self.start_button.config(command=callback)

    def set_map_click_callback(self, callback):
        self.map_widget.add_right_click_menu_command(
            label="Add Waypoint",
            command=lambda coords: callback(coords[0], coords[1]),
            pass_coords=True
        )

    def update_drone_marker(self, telemetry, drone_marker):
        lat = telemetry["lat"]
        lon = telemetry["lon"]
        if lat is not None and lon is not None:
            drone_marker.set_position(lat, lon)
            self.map_widget.set_position(lat, lon)