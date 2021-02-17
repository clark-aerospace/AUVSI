#!/usr/bin/env python3

import asyncio
import os

from Mission import MissionPlan
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    # Set path to planned mission directory
    #curr_path = os.path.dirname(__file__)
    #planned_mission_path = os.path.relpath('../controlcenter/planning/', curr_path)
    #print("Planned Mission Path: " + str(planned_mission_path))

    print('-- Getting home position')
    # Initialize dictionary to hold home postion
    home = {'latitude': 0.0, 'longitude': 0.0, 'altitude': 0.0}
    # Subscribe to home postion telemetry for one cycle recording home gps 
    # values, then exit
    async for home_position in drone.telemetry.home():
        home['latitude'] = home_position.latitude_deg
        home['longitude'] = home_position.longitude_deg
        home['altitude'] = home_position.relative_altitude_m
        break
    
    current_mission = MissionPlan('text.json', home)

    await drone.mission.set_return_to_launch_after_mission(True)

    # Upload raw mission command list to drone
    print("-- Uploading mission")
    await drone.mission_raw.upload_mission(current_mission.getMissionRawWaypoints())

    # Upload boundary fence polygon to drone
    print("-- Uploading boundary fence")
    await drone.geofence.upload_geofence(current_mission.getMissionGeofence())

    print("-- Uploads complete")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
