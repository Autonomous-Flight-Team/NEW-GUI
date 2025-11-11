import tkinter as tk
import tkintermapview


def create_right_panel(parent):
	"""Create and pack the right (MAP) panel inside the given parent (top_frame).

	Args:
		parent: the container (typically top_frame) to attach the right panel to.

	Returns:
		tk.Frame: the created right panel frame.
	"""
	right_panel = tk.Frame(
		parent,
		bg='lightgreen',
		width=360,
		height=230
	)
	right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=10)

	# Add a visible label at the top of the right panel for the map
	right_label = tk.Label(right_panel, text="MAP", font=("Segoe UI", 14, 'bold'), fg='black', bg='lightgreen')
	right_label.pack(side=tk.TOP, anchor='n', pady=(8, 4))

	# create map widget
	map_widget = tkintermapview.TkinterMapView(right_panel, width=360, height=230, corner_radius=0)
	map_widget.pack(fill=tk.BOTH, expand=True)
	# set current widget position and zoom
	map_widget.set_position(47.65821445872502, -122.30391059662294)  # McMahon
	map_widget.set_zoom(15)

	return right_panel
