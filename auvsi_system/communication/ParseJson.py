''' This class can be used to parse the mission file 
    returned by the competition server'''
import json

class ParseJsonFile:
    def __init__(self,jsonFile):
        # open json file
        self.jsonFile = json.loads(open(jsonFile).read())
        self.flyZonesList = self.jsonFile['flyZones'] 
        self.flyZoneDictionary = self.flyZonesList[0]

    def getFlyZoneList(self):
        self.flyZoneList = self.jsonFile['flyZones']
        return self.flyZoneList

    def getAltitudeMax(self):
        self.altitudeMax = self.flyZoneDictionary['altitudeMax']
        return self.altitudeMax

    def getAltitudeMin(self):
        self.altitudeMin = self.flyZoneDictionary['altitudeMin']
        return self.altitudeMin

    def getBoundaryPointList(self):
        self.boundaryPointsList = self.flyZoneDictionary['boundaryPoints']
        return self.boundaryPointsList
    
    def getWayPointList(self):
        self.wayPointsList = self.jsonFile['waypoints']
        return self.wayPointsList

    def getObstacleList(self):
        self.obstacleList = self.jsonFile['stationaryObstacles']
        return self.obstacleList

    def getAirDropPosition(self):
        self.airDropPosition = self.jsonFile['airDropPos']
        return self.airDropPosition
    
    def getAirDropBoundaryPoints(self):
        self.airDropBoundaryPoints = self.jsonFile['airDropBoundaryPoints']
        return self.airDropBoundaryPoints

    def getUGVDrivePosition(self):
        self.ugvDrivePosition = self.jsonFile['ugvDrivePos']
        return self.ugvDrivePosition

    def getSearchGrid(self):
        self.searchGrid = self.jsonFile['searchGridPoints']
        return self.searchGrid
