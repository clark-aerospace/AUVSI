''' create a list of missions and append MissionItem '''
from mavsdk.mission import (MissionItem)
from ConvertUnits import ConvertFootToMeter

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
                                        ConvertFootToMeter(altitude),
                                        16,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan')))
    return missionItems
