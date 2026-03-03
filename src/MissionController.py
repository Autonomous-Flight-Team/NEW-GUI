from mavsdk.mission import MissionItem, MissionPlan

class Waypoint:
    def __init__(self, lat, lon, alt=20.0, speed=5.0):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.speed = speed


class MissionController:
    def __init__(self, map_widget, mavsdk_manager):
        self.map_widget = map_widget
        self.mavsdk = mavsdk_manager

        self.waypoints = []
        self.markers = []
        self.path = None

    # --------------------------
    # Waypoint Management
    # --------------------------

    def add_waypoint(self, lat, lon):
        wp = Waypoint(lat, lon)
        self.waypoints.append(wp)

        marker = self.map_widget.set_marker(
            lat, lon, text=f"WP {len(self.waypoints)}"
        )
        self.markers.append(marker)

        self.update_path()

    def delete_last_waypoint(self):
        if not self.waypoints:
            return

        self.waypoints.pop()
        marker = self.markers.pop()
        marker.delete()

        self.update_path()
        for i, marker in enumerate(self.markers):
            marker.set_text(f"WP {i+1}")

    def clear_mission(self):
        for marker in self.markers:
            marker.delete()

        if self.path:
            self.path.delete()

        self.waypoints.clear()
        self.markers.clear()
        self.path = None

    def update_path(self):
        if self.path:
            self.path.delete()

        coords = [(wp.lat, wp.lon) for wp in self.waypoints]

        if len(coords) >= 2:
            self.path = self.map_widget.set_path(coords)

    # --------------------------
    # Drone Communication
    # --------------------------

    def upload_mission(self):
        if not self.waypoints:
            print("No waypoints to upload.")
            return

        self.mavsdk.upload_mission(self.waypoints)

    def start_mission(self):
        self.mavsdk.start_mission()