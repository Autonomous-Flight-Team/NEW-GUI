import tkinter as tk

class StatusBar:
    def __init__(self):
        self.labels = {}

    def create_status_bar(self, parent):
        bar = tk.Frame(parent, bg='#1a1a2e', height=28)
        bar.pack_propagate(False)

        font_cfg = ("Segoe UI", 10, "bold")

        def make_indicator(key, default_text, column):
            lbl = tk.Label(bar, text=default_text, font=font_cfg,
                           bg='#1a1a2e', fg='grey', anchor='center')
            lbl.pack(side=tk.LEFT, padx=12)
            self.labels[key] = lbl

        make_indicator("connection", "⬤  Disconnected", 0)
        make_indicator("armed",      "⬤  Disarmed",     1)
        make_indicator("mode",       "Mode: ---",       2)
        make_indicator("gps",        "GPS: ---",        3)
        make_indicator("battery",    "Battery: ---",    4)

        return bar

    def update_status(self, telemetry):
        # Connection
        if telemetry.get("is_connected"):
            self.labels["connection"].config(text="⬤  Connected", fg='#4CAF50')
        else:
            self.labels["connection"].config(text="⬤  Disconnected", fg='#f44336')

        # Armed
        if telemetry.get("is_armed"):
            self.labels["armed"].config(text="⬤  Armed", fg='#ff9800') #4CAF50
        else:
            self.labels["armed"].config(text="⬤  Disarmed", fg='#f44336')

        # Flight mode
        mode = telemetry.get("flight_mode")
        self.labels["mode"].config(
            text=f"Mode: {mode if mode else '---'}",
            fg='white'
        )

        # GPS
        sats = telemetry.get("gps_num_satellites")
        fix = telemetry.get("gps_fix_type", "---")
        gps_color = '#4CAF50' if sats and sats >= 6 else '#f44336'
        self.labels["gps"].config(
            text=f"GPS: {fix} ({sats if sats else '--'} sats)",
            fg=gps_color
        )

        # Battery
        pct = telemetry.get("battery_remaining")
        volts = telemetry.get("battery_voltage")
        if pct is not None:
            bat_color = '#4CAF50' if pct > 30 else '#ff9800' if pct > 15 else '#f44336'
            self.labels["battery"].config(
                text=f"Battery: {pct}% ({volts}V)",
                fg=bat_color
            )