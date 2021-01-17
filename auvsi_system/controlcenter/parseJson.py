''' This class can be used to parse the mission file 
    returned by the competition server'''
import json

class ParseJsonFile:
    def __init__(self,jsonFile):
        # open json file
        self.jsonFile = json.loads(open(jsonFile).read())
        self.flyZonesList = self.jsonFile['flyZones'] 
        self.flyZoneDictionary = self.flyZonesList[0]
        self.wayPointsList = self.jsonFile['waypoints']
        self.boundaryPointsList = self.flyZoneDictionary['boundaryPoints']
        self.searchPointList = self.jsonFile['searchGridPoints']
        self.altitudeMax = self.flyZoneDictionary['altitudeMax']
        self.altitudeMin = self.flyZoneDictionary['altitudeMin']

    def getFlyZoneList(self):
        self.flyZoneList = self.jsonFile['flyZones']
        return self.flyZoneList

    def getAltitudeMax(self):
        self.altitudeMax = self.flyZoneDictionary['altitudeMax']
        return self.altitudeMax

    def getAltitudeMin(self):
        self.altitudeMin = self.flyZoneDictionary['altitudeMin']
        return self.altitudeMin

    def getBoundaryPointList(self, index):
        self.boundaryPointsList = self.flyZoneDictionary['boundaryPoints']  # size of list can vary
        return self.boundaryPointsList[index]
    
    def getWayPointList(self):
        self.wayPointsList = self.jsonFile['waypoints']
        return self.wayPointsList
    
    @staticmethod
    def create_waypoints(path, coordinates):
        points = []

        for coord in coordinates:
            points += [{"longitude": coord[0], "latitude": coord[1]}]
        
        data = {"waypoints": points}

        with open(path, 'w') as f:
            f.write(json.dumps(data, indent = 2))
        
        return  data


