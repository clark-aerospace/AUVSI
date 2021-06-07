#!/usr/bin/env python3

import asyncio
import os

#from VehicleInfo import SystemInfo
from Mission import Mission
from mavsdk import System

async def run():
    droneAddress = "udp://:14540"
    drone = System()
    await drone.connect(system_address = droneAddress)
   
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

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

    current_mission = Mission('test_mission.json', home)

    # Upload raw mission command list to drone
    print("-- Uploading mission")
    await drone.mission_raw.upload_mission(current_mission.getMissionWaypoints())

    # Upload boundary fence polygon to drone
    print("-- Uploading boundary fence + obstalces")
    fenceList = current_mission.getMissionGeofence() + current_mission.getMissionObstacles()    
    await drone.geofence.upload_geofence(fenceList)

    print("-- Uploads complete")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
