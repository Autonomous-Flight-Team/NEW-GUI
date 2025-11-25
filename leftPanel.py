import tkinter as tk


def create_left_panel(parent):
    """Create and pack the left (Commands) panel inside the given parent (top_frame).

    Args:
        parent: the container (typically top_frame) to attach the left panel to.

    Returns:
        tk.Frame: the created left panel frame.
    """
    left_panel = tk.Frame(
        parent,
        bg='lightblue',
        width=100,
        height=230
    )
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)

    # Add a visible label at the top of the left panel for commands
    left_label = tk.Label(left_panel, text="COMMANDS", font=("Segoe UI", 14, 'bold'), fg='black', bg='lightblue')
    left_label.pack(side=tk.TOP, anchor='n', pady=(8, 4))

    return left_panel

