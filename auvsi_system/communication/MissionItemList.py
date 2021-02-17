''' create a list of missions and append MissionItem '''
from mavsdk.mission import MissionItem as MissionItem
from mavsdk.mission_raw import MissionItem as RawMissionItem
from mavsdk.geofence import (Point, Polygon) 
from ConvertUnits import ConvertFootToMeter

# accepts a list of dictionaries and returns a list of mission items
def WayPointMission(dictionaryList):
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
def RawWayPointMission(dictionaryList):
    rawMissionItems = []
    frame = 6
    autocontinue = 1
    param1 = 0.0
    param2 = 0.0
    param3 = 0.0
    param4 = float('nan')
    mission_type = 0
    for seq, dictionary in enumerate(dictionaryList):
        latitude = int(dictionary["latitude"]*10**7)
        longitude = int(dictionary["longitude"]*10**7)
        altitude =  ConvertFootToMeter(dictionary["altitude"])
        if seq == 0:
            command = 84 # command for vtol takeoff and transition
            current = 1 # TRUE flag for first mission waypoint 
        elif seq == len(dictionaryList) - 1:
            command = 85 # command for vtol transition and land
            current = 0 # FALSE flag for first mission waypoint
        else:
            command = 16 # command for standard mission waypoint
            current = 0 # FALSE flag for first mission waypoint

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
        
    return rawMissionItems

# Accepts a list of dictionaries and returns and returns a list of list 
# geofence points
def BoundaryPointPolygon(dictionaryList):
    geofencePointList = []

    # Convert boundary point dictionarie into mavsdk geofence points
    for dictionary in dictionaryList:
       geofencePoint = Point(dictionary["latitude"], dictionary["longitude"]) 
       geofencePointList.append(geofencePoint)
    
    # Create geofence polygon object
    geofencePolygon = Polygon(geofencePointList, Polygon.FenceType.INCLUSION)

    return [geofencePolygon]  
