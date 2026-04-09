import asyncio
import threading
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
import os

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
            "distance_from_home": None,
            "is_connected": False,
            "is_armed": False,
            "flight_mode": None,
            "gps_fix_type": None,
            "gps_num_satellites": None,
            "battery_voltage": None,
            "battery_remaining": None
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
        # port = "/dev/cu.PL2303G-USBtoUART110"
        port = "/dev/cu.usbserial-AB998Y3J"
        
        if not os.path.exists(port):
            print(f"ERROR: Serial port {port} not found.")
            print("Available ports:")
            import glob
            for p in glob.glob('/dev/tty.*'):
                print(f"  {p}")
            return
        
        print("Connecting to drone...")
        await self.drone.connect(system_address=f"serial://{port}:460800")
        self.drone._sysid = 10

        # Simulation testing
        # await self.drone.connect(system_address="udp://:14540")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("Connected to drone!")
                break

        # try:
        #     async with asyncio.timeout(10):  # 10 second timeout
        #         async for state in self.drone.core.connection_state():
        #             if state.is_connected:
        #                 print("Connected to drone!")
        #                 break
        # except asyncio.TimeoutError:
        #     print("Connection timed out. Check port, baud rate, and cable.")
        #     return  # Exit early — don't start streams


        # start telemetry streams, each runs concurrently in infinite async loops
        asyncio.create_task(self.stream_position())
        asyncio.create_task(self.stream_velocity())
        asyncio.create_task(self.stream_attitude())
        # asyncio.create_task(self.stream_connection())
        asyncio.create_task(self.stream_armed())
        asyncio.create_task(self.stream_flight_mode())
        asyncio.create_task(self.stream_gps())
        asyncio.create_task(self.stream_battery())
        asyncio.create_task(self.monitor_connection())

        self.telemetry["is_connected"] = True

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

    async def stream_armed(self):
        async for is_armed in self.drone.telemetry.armed():
            self.telemetry["is_armed"] = is_armed

    async def stream_flight_mode(self):
        async for mode in self.drone.telemetry.flight_mode():
            self.telemetry["flight_mode"] = str(mode).replace("FlightMode.", "")

    async def stream_gps(self):
        async for gps in self.drone.telemetry.gps_info():
            self.telemetry["gps_fix_type"] = str(gps.fix_type)
            self.telemetry["gps_num_satellites"] = gps.num_satellites

    async def stream_battery(self):
        async for battery in self.drone.telemetry.battery():
            self.telemetry["battery_voltage"] = round(battery.voltage_v, 2)
            self.telemetry["battery_remaining"] = round(battery.remaining_percent * 100, 1)

    # async def stream_connection(self):
    #     async for state in self.drone.core.connection_state():
    #         self.telemetry["is_connected"] = state.is_connected
    async def monitor_connection(self):
        # Monitor for disconnection after initial connect
        await asyncio.sleep(1)  # Let initial connection settle
        async for state in self.drone.core.connection_state():
            self.telemetry["is_connected"] = state.is_connected
            if not state.is_connected:
                print("WARNING: Drone disconnected.")

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