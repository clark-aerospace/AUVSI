''' 
This is the class that contains all parsed interop mission items that can be
transferred to a UAV. The class contains methods to parse mission json files 
(including: mission waypoints, boundary fences, obstacles, etc) into mavlink 
compatible messages as well as methods to print out different mission items
'''

from parseJson import ParseJsonFile
from mavsdk.mission_raw import MissionItem as RawMissionItem
from mavsdk.geofence import (Point, Polygon) 
from pygeodesy.ellipsoidalVincenty import LatLon



class Mission:
    def __init__(self, jsonFile, homePosition):
        self.jsonFile = ParseJsonFile(jsonFile)
        self.home = homePosition
        self.waypointList = self.jsonFile.getWayPointList()
        self.boundaryPoints = self.jsonFile.getBoundaryPointList()
        self.obstacles = self.jsonFile.getObstacleList()
        self.airDropPosition = self.jsonFile.getAirDropPosition()
        self.airDropBoundarPoints = self.jsonFile.getAirDropBoundaryPoints()
        self.ugvDrivePosition = self.jsonFile.getUGVDrivePosition()
        self.searchGrid = self.jsonFile.getSearchGrid()
        # Add the home position to the end of the waypoint list
        self.waypointList.append(self.home)
               
    def getMissionWaypoints(self):
        '''
        Returns a list of raw mission waypoint items
        '''

        self.missionWaypoints = convertToWaypointMission(self.waypointList)
        return self.missionWaypoints

    def getMissionGeofence(self):
        '''
        Returns a list of geofence polygons, each containing geofence points and 
        fence type
        '''

        self.missionGeofence = convertToBoundaryPointPolygon(self.boundaryPoints)
        return self.missionGeofence

    def getMissionObstacles(self):
        '''
        Returns a list of geofence polygons, each containing a circular obstacle represented
        as an EXCLUSION zone polygon
        '''

        self.missionObstacles = convertToObstaclePolygons(self.obstacles)
        return self.missionObstacles

    def getMissionWaypointArray(self):
        '''
        Returns a list of lists version of the mission waypoints, currently used
        by InformedRRTStar. Currently configured to return 2D array. **Will upgrade
        to 3D**
        '''

        waypointArray = []
        for waypoint in self.waypointList:
            waypointArray.append([waypoint["longitude"], waypoint["latitude"]])

        return waypointArray

    def getMissionObstacleArray(self):

        obstacleArray = []
        for obstacle in self.obstacles:
            obstacleArray.append([obstacle["longitude"], obstacle["latitude"]])

        return obstacleArray

    def getMissionGeofenceArray(self):

        boundaryPointArray = []
        for boundaryPoint in self.boundaryPoints:
            boundaryPointArray.append([boundaryPoint["longitude"], boundaryPoint["latitude"]])

        return boundaryPointArray

    @staticmethod
    def ConvertFootToMeter(foot):
        '''This is a helper function which takes in a measurement in feet and 
            returns a measurement in meters'''
        # Multiply the input value by the conversion factor and return it
        return foot*0.3048   

    @staticmethod
    def vtolTakeoffWaypoint(seq, lat, lon, alt, frame = 6, current = 1, auto = 1):
    # Defines a raw mavlink VTOL takeoff waypoint
        command = 84
        param1 = 0.0
        param2 = 0.0
        param3 = 0.0
        param4 = float('nan')
        mission_type = 0
        return MissionItem(seq, frame, command, current, auto, 
                           param1, param2, param3, param4, 
                           lat, lon, alt, mission_type)
    @staticmethod  
    def vtolLandWaypoint(seq, lat, lon, alt, frame = 6, current = 0, auto = 1):
    # Defines a raw mavlink VTOL land waypoint
        command = 85
        param1 = 0.0
        param2 = 0.0
        param3 = 0.0
        param4 = float('nan')
        mission_type = 0
        return MissionItem(seq, frame, command, current, auto,
                           param1, param2, param3, param4,
                           lat, lon, alt, mission_type)
    @staticmethod 
    def standardWaypoint(seq, lat, lon, alt, frame = 6, current = 0, auto = 1):
    # Defines a raw mavlink standard waypoint
        command = 16
        param1 = 0.0
        param2 = 0.0
        param3 = 0.0
        param4 = float('nan')
        mission_type = 0
        return MissionItem(seq, frame, command, current, auto,
                            param1, param2, param3, param4,
                            lat, lon, alt, mission_type)

    @staticmethod
    def convertToWaypointMission(waypointList):
        '''
        Accepts a list of waypoint dictionaries and returns a list of raw mission items
        '''

        MissionItems = []
        for seq, waypoint in enumerate(waypointList):
            latitude = int(waypoint["latitude"]*10**7)
            longitude = int(waypoint["longitude"]*10**7)
            altitude =  ConvertFootToMeter(waypoint["altitude"])
            if seq == 0:
                current_waypoint = vtolTakeoffWaypoint(seq, latitude, longitude, altitude)
            elif seq == len(waypointList) - 1:
                current_waypoint = vtolLandWaypoint(seq, latitude, longitude, altitude)
            else:
                current_waypoint = standardWaypoint(seq, latitude, longitude, altitude)
    
            MissionItems.append(current_waypoint)
            
        return MissionItems
    
    @staticmethod
    def convertToBoundaryPointPolygon(boundaryPointList):
        '''
        Accepts a list of boundary point dictionaries and returns a list of list 
        mavsdk geofence polygons
        '''

        geofencePointList = []
    
        # Convert boundary point dictionarie into mavsdk geofence points
        for boundaryPoint in boundaryPointList:
           geofencePoint = Point(boundaryPoint["latitude"], boundaryPoint["longitude"]) 
           geofencePointList.append(geofencePoint)
        
        # Create geofence polygon object
        geofencePolygon = Polygon(geofencePointList, Polygon.FenceType.INCLUSION)
    
        return [geofencePolygon]  
    
    @staticmethod
    def convertToObstaclePolygons(obstacleList, numVertices = 8):
        '''
        Accepts a list of obstacle dictionaries and returns a list of mavsdk compatible 
        obstacle polygons
        '''

        # Initialize list to hold obstacle polygons
        obstaclePolygonList = []
    
        for obstacle in obstacleList:
            # Initialize list to hold points in each obstacle polygon
            obstaclePointList = []
            # Capture data from the current obstacle
            latitude = obstacle["latitude"]
            longitude = obstacle["longitude"]
            radius = ConvertFootToMeter(obstacle["radius"])
            # Initialize ellipsoidal Vincenty point
            obstaclePoint = LatLon(latitude, longitude)
            # For each vertex point in the polygon that represents the circular obstacle
            for index in range(numVertices):
                # Calculate the azimuth angle of the vertex
                angle = index * 360 / numVertices
                # Calculate the gps coordinate of the vertex based off the obstacles 
                # radius and azimuth angle
                vertex = obstaclePoint.destination(radius, angle)
                vertexPoint = Point(float(vertex.lat), float(vertex.lon))
                obstaclePointList.append(vertexPoint)
    
            # Append the current obstacle polygon to the obstaclePolygonList
            obstaclePolygon = Polygon(obstaclePointList, Polygon.FenceType.EXCLUSION)
            obstaclePolygonList.append(obstaclePolygon)

        return obstaclePolygonList

    def printWaypointList(self):
        print(self.waypointList)

    def printBoundaryPoints(self):
        print(self.boundaryPoints)

    def printObstaclePoints(self):
        print(self.obstacles)
