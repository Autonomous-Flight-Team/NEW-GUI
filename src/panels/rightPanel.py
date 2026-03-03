import tkinter as tk
import tkintermapview

class RightPanel: 

	def create_right_panel(self, parent):
		"""Create and pack the right (MAP) panel inside the given parent (top_frame).

		Args:
			parent: the container (typically top_frame) to attach the right panel to.

		Returns:
			tk.Frame: the created right panel frame.
		"""
		right_panel = tk.Frame(
			parent,
			bg='lightblue',
			width=360,
			height=230
		)
		right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=10)

		right_label = tk.Label(right_panel, text="MAP", font=("Segoe UI", 14, 'bold'), fg='black', bg='lightblue')
		right_label.pack(side=tk.TOP, anchor='n', pady=(8, 4))

		# create map widget
		map_widget = tkintermapview.TkinterMapView(right_panel, width=360, height=230, corner_radius=0)
		map_widget.pack(fill=tk.BOTH, expand=True)
		# set current widget position and zoom
		#map_widget.set_position(47.65821445872502, -122.30391059662294)  # McMahon
		map_widget.set_zoom(15)

		button_frame = tk.Frame(right_panel, bg="lightblue")
		button_frame.pack(fill=tk.X, pady=5)

		upload_button = tk.Button(
			button_frame,
			text="Upload Mission",
			command=lambda: None
		)
		upload_button.pack(side=tk.LEFT, padx=5)

		start_button = tk.Button(
			button_frame,
			text="Start Mission",
			command=lambda: None
		)
		start_button.pack(side=tk.LEFT, padx=5)

		drone_marker = map_widget.set_marker(
			0, 0,
			text="DRONE",
			marker_color_circle="red",
			marker_color_outside="white"
		)
		
		self.map_widget = map_widget

		return right_panel, drone_marker, map_widget
	
	def update_drone_marker(self, telemetry, drone_marker, map_widget):
		lat = telemetry["lat"]
		lon = telemetry["lon"]
		if lat is not None and lon is not None:
			drone_marker.set_position(lat, lon)
			map_widget.set_position(lat, lon)

	def connect_mission_controller(self, mission_controller):
			# Wire buttons
			for widget in self.map_widget.master.winfo_children():
				if isinstance(widget, tk.Frame):
					for child in widget.winfo_children():
						if isinstance(child, tk.Button):
							if child["text"] == "Upload Mission":
								child.config(command=mission_controller.upload_mission)
							elif child["text"] == "Start Mission":
								child.config(command=mission_controller.start_mission)

			# Wire map click
			self.map_widget.add_right_click_menu_command(
				label="Add Waypoint",
				command=lambda coords: mission_controller.add_waypoint(coords[0], coords[1]),
				pass_coords=True
			)