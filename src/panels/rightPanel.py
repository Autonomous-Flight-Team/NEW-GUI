import tkinter as tk
import tkintermapview
from datetime import datetime


class RightPanel:

    def __init__(self):
        self.map_widget = None
        self.upload_button = None
        self.start_button = None
        self.status_log = None
        self._map_frame = None
        self._status_frame = None
        self._view_var = None

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

        #-------------------#
        # Drop Down
        #-------------------#
        dropdown_frame = tk.Frame(right_panel, bg='lightblue')
        dropdown_frame.pack(fill=tk.X, padx=5, pady=(0, 4))

        tk.Label(
            dropdown_frame,
            text="View:",
            font=("Segoe UI", 10),
            bg='lightblue'
        ).pack(side=tk.LEFT, padx=(0, 4))

        self._view_var = tk.StringVar(value="Map")
        view_menu = tk.OptionMenu(
            dropdown_frame,
            self._view_var,
            "Map",
            "MAVLink Status Board",
            command=self._switch_view
        )
        view_menu.config(font=("Segoe UI", 10), bg='white', relief='flat')
        view_menu.pack(side=tk.LEFT)

        #-------------------#
        # map frame
        #-------------------#
        self._map_frame = tk.Frame(right_panel, bg='lightblue')
        self._map_frame.pack(fill=tk.BOTH, expand=True)

        self.map_widget = tkintermapview.TkinterMapView(
            self._map_frame,
            corner_radius=0
        )
        self.map_widget.pack(fill=tk.BOTH, expand=True)
        self.map_widget.set_zoom(15)

        # Buttons (live inside map frame so they hide with the map)
        button_frame = tk.Frame(self._map_frame, bg="lightblue")
        button_frame.pack(fill=tk.X, pady=5)

        self.upload_button = tk.Button(button_frame, text="Upload Mission", highlightbackground='light blue')
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(button_frame, text="Start Mission", highlightbackground='light blue')
        self.start_button.pack(side=tk.LEFT, padx=5)


        #-----------------------------#
        # MAVLink Status Board frame
        #-----------------------------#
        self._status_frame = tk.Frame(right_panel, bg='lightblue')
        # (not packed yet — hidden by default)

        status_label = tk.Label(
            self._status_frame,
            text="MAVLink Status Board",
            font=("Segoe UI", 11, 'bold'),
            fg='#1f77b4',
            bg='lightblue'
        )
        status_label.pack(pady=(6, 2))

        log_frame = tk.Frame(self._status_frame, bg='lightblue')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 8))

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Black Frame for the messages to be displayed.
        self.status_log = tk.Text(
            log_frame,
            state='disabled',
            bg='#1e1e1e',  # <--- black background color
            fg='#00ff00',
            font=("Courier New", 10),
            yscrollcommand=scrollbar.set,
            relief='flat',
            wrap='word'
        )

        # Test print message on status board
        self.log_status("Hello, this is a test message!")

        self.status_log.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.status_log.yview)
       
        #-----------------------------#
        # Drone marker placeholder
        #-----------------------------#
        drone_marker = self.map_widget.set_marker(
            0, 0,
            text="DRONE",
            marker_color_circle="red",
            marker_color_outside="white"
        )

        return right_panel, drone_marker

    #-------------------#
    # View switching
    #-------------------#
    def _switch_view(self, selection):
        if selection == "Map":
            self._status_frame.pack_forget()
            self._map_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self._map_frame.pack_forget()
            self._status_frame.pack(fill=tk.BOTH, expand=True)

    #-----------------------#
    # Public wiring methods
    #-----------------------#
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

    #----------------------#
    # MAVLink Status Board
    #----------------------#
    def log_status(self, message: str):
        """Append a timestamped message to the MAVLink status log."""
        if self.status_log is None:
            print(message)
            return

        timestamp = datetime.now().strftime("%H:%M:%S")

        def _write():
            self.status_log.config(state='normal')
            self.status_log.insert('end', f"[{timestamp}] {message}\n")
            self.status_log.see('end')
            self.status_log.config(state='disabled')

        self.status_log.after(0, _write)