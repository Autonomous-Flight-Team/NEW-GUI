import tkinter as tk


def create_bottom_panel(parent):
    """Create and pack the bottom data panel inside the given parent (typically root).

    Args:
        parent: the container (usually the main root) to attach the bottom panel to.

    Returns:
        tk.Frame: the created bottom panel frame.
    """
    bottom_panel = tk.Frame(
        parent,
        bg='lightgrey',
        width=540,
        height=150
    )
    bottom_panel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Add a visible label at the top of the bottom panel for telemetry/data
    bottom_label = tk.Label(bottom_panel, text="DATA - Altitude, Speed, Heading", font=("Segoe UI", 13, 'bold'), fg='black', bg='lightgrey')
    bottom_label.pack(side=tk.TOP, anchor='n', pady=(6, 4))

    return bottom_panel