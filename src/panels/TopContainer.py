import tkinter as tk

class TopContainer:

	def create_top_container(self, root):
		"""Create and return the top container Frame that holds the left and right panels.

		Args:
			root: the main Tk root or parent widget.

		Returns:
			tk.Frame: the packed top container frame.
		"""
		top_frame = tk.Frame(root)
		return top_frame