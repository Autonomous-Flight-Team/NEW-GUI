import tkinter as tk


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

	return right_panel
