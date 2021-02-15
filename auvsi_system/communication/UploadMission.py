#!/usr/bin/env python3

import asyncio
import os

from mavsdk import System
from parseJson import ParseJsonFile
from MissionItemList import RawWayPointsMission

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    # Set path to planned mission directory
    curr_path = os.path.dirname(__file__)
    planned_mission_path = os.path.relpath('../controlcenter/planning/', curr_path)
    print("Planned Mission Path: " + str(planned_mission_path))

    # Reconfigure this line to parse mission file that has been run through the
    # path planning algorithm
    jsonFile = ParseJsonFile('text.json')
    wayPointList = jsonFile.getWayPointList()

    # Need to also parse mission fence, obstacles and drop zone submission.
    # Either the planned mission needs this data present or a seperate file
    # containing the relevant data needs to be opened

    print('-- Getting home position')
    home = {'latitude': 0.0, 'longitude': 0.0, 'altitude': 0.0}
    async for home_position in drone.telemetry.home():
        home['latitude'] = home_position.latitude_deg
        home['longitude'] = home_position.longitude_deg
        home['altitude'] = home_position.relative_altitude_m
        break
    
    wayPointList.append(home)

    print(wayPointList)

    mission_plan = RawWayPointsMission(wayPointList)
    print('len of mission: ' + str(len(mission_plan)))

    await drone.mission.set_return_to_launch_after_mission(True)


    print("-- Uploading mission")
    await drone.mission_raw.upload_mission(mission_plan)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
