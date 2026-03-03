import asyncio
import threading
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan

class MAVSDKManager:
    def __init__(self):
        self.drone = System()
        self.loop = asyncio.new_event_loop()
        #create background thread
        self.thread = threading.Thread(target=self.start_event_loop, daemon=True)

        # Telemetry storage (GUI reads these)
        self.telemetry = {
            "lat": None,
            "lon": None,
            "altitude": None,
            "ground_speed": None,
            "yaw": None,
            "vertical_speed": None,
            "distance_to_wp": None,
            "distance_from_home": None
        }

    # starts baackground thread
    def start(self):
        self.thread.start()

    # runs inside background thread
    def start_event_loop(self):
        asyncio.set_event_loop(self.loop)
        # starts the asyncio loop
        self.loop.create_task(self.connect_and_start_streams())
        self.loop.run_forever()

    async def connect_and_start_streams(self):
        # connect to px4
        print("Connecting to PX4...")
        await self.drone.connect(system_address="udp://:14540")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("Connected to drone!")
                break

        # start telemetry streams, each runs concurrently in infinite async loops
        asyncio.create_task(self.stream_position())
        asyncio.create_task(self.stream_velocity())
        asyncio.create_task(self.stream_attitude())

    async def stream_position(self):
        async for pos in self.drone.telemetry.position():
            self.telemetry["lat"] = pos.latitude_deg;
            self.telemetry["lon"] = pos.longitude_deg;
            self.telemetry["altitude"] = round(pos.relative_altitude_m, 2)

    async def stream_velocity(self):
        # ned = north east down coord system. Velocity in m/s
        async for vel in self.drone.telemetry.velocity_ned():
            #pythagorean theorem speed = sqrt(north² + east²)
            hor_speed = (vel.north_m_s**2 + vel.east_m_s**2) ** 0.5
            self.telemetry["ground_speed"] = round(hor_speed, 2)
            self.telemetry["vertical_speed"] = round(vel.down_m_s, 2)

    async def stream_attitude(self):
        # euler angles: yaw, pitch, roll
        async for att in self.drone.telemetry.attitude_euler():
            self.telemetry["yaw"] = round(att.yaw_deg, 1)

    def build_mission_plan(self, waypoints):
        mission_items = []

        for wp in waypoints:
            item = MissionItem(
                latitude_deg=wp.lat,
                longitude_deg=wp.lon,
                relative_altitude_m=wp.alt,
                speed_m_s=wp.speed,
                is_fly_through=True,
                gimbal_pitch_deg=0.0,
                gimbal_yaw_deg=0.0,
                camera_action=MissionItem.CameraAction.NONE,
                loiter_time_s=0,
                camera_photo_interval_s=0,
                acceptance_radius_m=1600,
                yaw_deg=0,
                camera_photo_distance_m=0,
                vehicle_action='TakeOff'
                    #TransitionToFw: When a waypoint is reached vehicle will transition to fixed-wing mode.
                    #TransitionToMc: When a waypoint is reached vehicle will transition to multi-copter mode.

            )
            mission_items.append(item)

        return MissionPlan(mission_items)
    
    def upload_mission(self, waypoints):
        mission_plan = self.build_mission_plan(waypoints)

        asyncio.run_coroutine_threadsafe(
            self._upload_mission_async(mission_plan),
            self.loop
        )

    async def _upload_mission_async(self, mission_plan):
        print("Uploading mission...")
        await self.drone.mission.clear_mission()
        await self.drone.mission.upload_mission(mission_plan)
        print("Mission uploaded successfully.")

    def start_mission(self):
        asyncio.run_coroutine_threadsafe(
            self._start_mission_async(),
            self.loop
        )

    async def _start_mission_async(self):
        print("Arming...")
        await self.drone.action.arm()

        print("Starting mission...")
        await self.drone.mission.start_mission()

        print("Mission started.")