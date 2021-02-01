#!/usr/bin/env python3

import asyncio

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

    print_mission_progress_task = asyncio.ensure_future(print_mission_progress(drone))

    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(observe_is_in_air(drone, running_tasks))

    # Reconfigure this line to parse mission file that has been run through the
    # path planning algorithm
    jsonFile = ParseJsonFile('text.json')
    wayPointList = jsonFile.getWayPointList()

    # Need to also parse mission fence, obstacles and drop zone submission

    print(wayPointList)
    print('len of mission: ' + str(len(WayPointsMission(wayPointList))))
    mission_plan = MissionPlan(WayPointsMission(wayPointList))

    await drone.mission.set_return_to_launch_after_mission(True)


    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

'''
    This will be removed as intent of the program is to only upload planned
    missions to the aircraft. Primary operation of the UAV will be performed
    from QGroundControl, not from another piece of software.

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting mission")
    await drone.mission.start_mission()

    await termination_task

async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")


async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return
'''


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
