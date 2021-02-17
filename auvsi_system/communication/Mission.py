''' 
This is the class that contains all parsed interop mission items that can be
transferred to a UAV. The class contains methods to parse mission json files 
(including: mission waypoints, boundary fences, obstacles, etc) into mavlink 
compatible messages as well as methods to print out different mission items
'''

from parseJson import ParseJsonFile
from MissionItemList import RawWayPointMission, BoundaryPointPolygon

class MissionPlan:
    def __init__(self, jsonFile, homePosition):
        self.jsonFile = ParseJsonFile(jsonFile)
        self.home = homePosition
        self.waypointList = self.jsonFile.getWayPointList()
        self.boundaryPoints = self.jsonFile.getBoundaryPointList()
        # Add the home position to the end of the waypoint list
        self.waypointList.append(self.home)
        self.missionWaypoints = RawWayPointMission(self.waypointList)
        self.missionGeofence = BoundaryPointPolygon(self.boundaryPoints)

    # Returns a list of raw mission waypoint items
    def getMissionRawWaypoints(self):
        return self.missionWaypoints

    # Returns a list of geofence polygons, each containing geofence points and 
    # fence type
    def getMissionGeofence(self):
        return self.missionGeofence

    def printWaypointList(self):
        print(self.waypointList)

    def printBoundaryPoints(self):
        print(self.boundaryPoints)
