import sys
sys.path.insert(1, "/interop/client")

from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
from google.protobuf.json_format import MessageToJson

client = client.Client(url='http://127.0.0.1:8000',
                       username='testuser',
                       password='testpass')

mission = client.get_mission(1)
'''
mission_obj = {}
mission_obj['id'] = mission.id
mission_obj['lostCommsPos'] = mission.lost_comms_pos
mission_obj['flyZones'] = mission.fly_zones
mission_obj['waypoints'] = mission.waypoints
mission_obj['searchGridPoints'] = mission.search_grid_points
mission_obj['stationaryObstacles'] = mission.stationary_obstacles
'''

print(MessageToJson(mission))

