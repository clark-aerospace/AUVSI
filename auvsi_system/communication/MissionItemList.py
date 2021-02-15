''' create a list of missions and append MissionItem '''
from mavsdk.mission import MissionItem as MissionItem
from mavsdk.mission_raw import MissionItem as RawMissionItem
from ConvertUnits import ConvertFootToMeter

# accepts a list of dictionaries and returns a list of mission items
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

# accepts a list of dictionaries and returns a list of raw mission items
def RawWayPointsMission(dictionaryList):
    rawMissionItems = []
    seq = 0
    frame = 6
    autocontinue = 1
    param1 = 0.0
    param2 = 0.0
    param3 = 0.0
    param4 = float('nan')
    mission_type = 0
    for dictionary in dictionaryList:
        latitude = int(dictionary["latitude"]*10**7)
        longitude = int(dictionary["longitude"]*10**7)
        altitude =  ConvertFootToMeter(dictionary["altitude"])
        if seq == 0:
            command = 84 # command for vtol takeoff and transition
            current = 1
        elif seq == len(dictionaryList) - 1:
            command = 85
            current = 0
        else:
            command = 16 
            current = 0

        rawMissionItems.append(RawMissionItem(seq,
                                            frame,
                                            command,
                                            current,
                                            autocontinue,
                                            param1,
                                            param2,
                                            param3,
                                            param4,
                                            latitude,
                                            longitude,
                                            altitude,
                                            mission_type))
        seq += 1
        
    return rawMissionItems
