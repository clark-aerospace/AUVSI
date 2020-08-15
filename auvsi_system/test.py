import sys
sys.path.insert(1, "/interop/client")

from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2


client = client.Client(url='http://127.0.0.1:8000',
                       username='testuser',
                       password='testpass')


mission = client.get_mission(1)
print(mission)


