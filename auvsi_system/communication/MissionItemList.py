''' create a list of missions and append MissionItem '''
from mavsdk.mission import (MissionItem)
# accepts a list of dictionaries and returns a list of missions
def WayPointsMission(dictionaryList):
    missionItems = []
    index = 0
    for dictionary in dictionaryList:
        latitude = dictionary["latitude"]
        longitude = dictionary["longitude"]
        altitude =  dictionary["altitude"]
        missionItems.append(MissionItem(latitude,
                                        longitude,
                                        altitude,
                                        10,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan')))
        if index > 4:
            break
        index += 1
    return missionItems
