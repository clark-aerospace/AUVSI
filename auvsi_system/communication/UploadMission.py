#!/usr/bin/env python3

import asyncio
import os

from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)
from parseJson import ParseJsonFile
from MissionItemList import WayPointsMission

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

    print(wayPointList)
    print('len of mission: ' + str(len(WayPointsMission(wayPointList))))
    mission_plan = MissionPlan(WayPointsMission(wayPointList))

    await drone.mission.set_return_to_launch_after_mission(True)


    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
