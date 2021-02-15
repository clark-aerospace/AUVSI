#!/usr/bin/env python3

import asyncio
import os

from mavsdk import System
from mavsdk import mission_raw

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("-- Downloading mission")
    mission_plan = await drone.mission_raw.download_mission()
    
    for mission_item in mission_plan:
        print(mission_item)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
