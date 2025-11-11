import tkinter as tk


def create_top_container(root):
	"""Create and return the top container Frame that holds the left and right panels.

	Args:
		root: the main Tk root or parent widget.

	Returns:
		tk.Frame: the packed top container frame.
	"""
	top_frame = tk.Frame(root)
	top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
	return top_frame