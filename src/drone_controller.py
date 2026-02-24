import asyncio
from mavsdk import System

class DroneController:
    def _init_(self):
        self.drone = System()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Connect immediately
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        print("Connecting to drone...")
        await self.drone.connect(system_address="udp://:14540")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("Connected to drone!")
                break
    
    def run(self, coroutine):
        """Runs async MAVSDK calls safely"""
        return self.loop.run_until_complete(coroutine)
    
    async def arm(self):
        await self.drone.action.arm()

    async def takeoff(self):
        await self.drone.takeoff()

    async def land(self):
        await self.drone.action.land()
