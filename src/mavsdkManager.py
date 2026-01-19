import asyncio
import threading
from mavsdk import System

class MAVSDKManager:
    def __init__(self):
        self.drone = System()
        self.loop = asyncio.new_event_loop()
        #create background thread
        self.thread = threading.Thread(target=self.start_event_loop, daemon=True)

        # Telemetry storage (GUI reads these)
        self.telemetry = {
            "altitude": None,
            "ground_speed": None,
            "yaw": None,
            "vertical_speed": None,
            "distance_to_wp": None,
            "distance_from_home": None
        }

    #starts baackground thread
    def start(self):
        self.thread.start()

    #runs inside background thread
    def start_event_loop(self):
        asyncio.set_event_loop(self.loop)
        #starts the asyncio loop
        #self.loop.run_until_complete(self.connect_and_start_streams())
        self.loop.create_task(self.connect_and_start_streams())
        self.loop.run_forever()

    async def connect_and_start_streams(self):
        #connect to px4
        print("Connecting to PX4...")
        await self.drone.connect(system_address="udp://:14540")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("Connected to drone!")
                break

        #start telemetry streams, each runs concurrently in infinite async loops
        asyncio.create_task(self.stream_position())
        asyncio.create_task(self.stream_velocity())
        asyncio.create_task(self.stream_attitude())

    async def stream_position(self):
        async for pos in self.drone.telemetry.position():
            self.telemetry["altitude"] = round(pos.relative_altitude_m, 2)

    async def stream_velocity(self):
        #ned= north east down coord system. Velocity in m/s
        async for vel in self.drone.telemetry.velocity_ned():
            #pythagorean theorem speed=sqrt(north² + east²)
            hor_speed = (vel.north_m_s**2 + vel.east_m_s**2) ** 0.5
            self.telemetry["ground_speed"] = round(hor_speed, 2)
            self.telemetry["vertical_speed"] = round(vel.down_m_s, 2)

    async def stream_attitude(self):
        #euler angles: yaw, pitch, roll
        async for att in self.drone.telemetry.attitude_euler():
            self.telemetry["yaw"] = round(att.yaw_deg, 1)