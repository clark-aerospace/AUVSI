from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from google.protobuf.json_format import MessageToJson
from .forms import InteropServerForm, MainPageForm
from .models import InteropServer
from .connect import connect
from .parseJson import ParseJsonFile
import sys
import os
import json
import math

from path_planner.simulator.simulator import Simulator
from path_planner.loader.loader import Loader
from path_planner.algorithms.astar.multithread import Astar as AstarAsync
from path_planner.algorithms.dijkstra.multithread import Dijkstra as DijkstraAsync

sys.path.insert(1, "/interop/client")
from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2


def connectionPage(request):
    if(request.method=='POST'):
        form = InteropServerForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('controlCenter')
    else:
        form = InteropServerForm()
    return render(request,'controlcenter/startConnection.html',{'form':form})

def controlCenter(request):
    if(request.method=='POST'):
        form = MainPageForm(request.POST)
        if(form.is_valid()):
            data = form.cleaned_data
            flush_data = data['flush_data']
            # check if InteropServer data needs to be flushed
            if(flush_data == "flush"):
                InteropServer.objects.all().delete()
            return redirect('controlCenter')
    else:
        form = MainPageForm()
    return render(request,'controlcenter/controlCenter.html',{'form': form})

def getMission(request):
    server = InteropServer.objects.all()[0]
    auvsi_client = client.Client(url=server.url,
                       username=server.username,
                       password=server.password)

    auvsi_client = client.Client(url='http://127.0.0.1:8000',
                       username='testuser',
                       password='testpass')

    mission = auvsi_client.get_mission(1)
    with open('controlcenter/missions/mission_file.json', 'w') as mission_file:
        mission_file.write(MessageToJson(mission))

    mission_file = ParseJsonFile(os.getcwd() + '/controlcenter/missions/mission_file.json')
    maxAltitude = mission_file.altitudeMax
    minAltitude = mission_file.altitudeMin
    wayPointsDict = constructDict(mission_file.wayPointsList, 3)
    boundaryDict = constructDict(mission_file.boundaryPointsList, 3)
    searchPointsDict = constructDict(mission_file.searchPointList, 3)
    return render(request,'controlcenter/get_mission.html',{'way_points_dict':wayPointsDict,'max_altitude':maxAltitude,'min_altitude':minAltitude,'boundary_dict':boundaryDict, 'search_dict':searchPointsDict})


def constructDict(list, columns):
    dict = {}
    rowNum = (math.ceil(len(list)/columns))
    index = 0
    for i in range(rowNum):
        row = []
        for x in range(columns):
            try:
                row.append(list[index])
                index += 1
            except Exception as e:
                break
        dict[i] = row
    return dict

def plan_mission(request):    
    return render(request, 'controlcenter/planMission.html')
    
def run_dijkstra(request):
    mission_file = os.getcwd() + '/controlcenter/missions/mission_file.json'
    plan_file = os.getcwd() + '/controlcenter/planning/dijkstra_planning.json'

    loader = Loader(mission_file, cartesian=False)
    algo = DijkstraAsync(loader)
    simulator = Simulator(loader)

    coordinates = simulator.simulate(algo, headless=True)
    print(coordinates)

    mission = ParseJsonFile(mission_file).jsonFile,
    plan = ParseJsonFile.create_waypoints(plan_file, coordinates)


    return render(request,'controlcenter/dijkstraMap.html',{'mission': mission[0], 'plan': plan})

def run_astar(request):
    mission_file = os.getcwd() + '/controlcenter/missions/mission_file.json'
    plan_file = os.getcwd() + '/controlcenter/planning/astar_planning.json'

    loader = Loader(mission_file, cartesian=False)
    algo = AstarAsync(loader)
    simulator = Simulator(loader)

    coordinates = simulator.simulate(algo, headless=True)
    print(coordinates)

    mission = ParseJsonFile(mission_file).jsonFile,
    plan = ParseJsonFile.create_waypoints(plan_file, coordinates)


    return render(request,'controlcenter/astarMap.html',{'mission': mission[0], 'plan': plan})


# this calls could look into the planning folder and determine if another alogorithim is ready for plotting
def boundaryGrid(request):
    mission_file = ParseJsonFile(os.getcwd() + '/controlcenter/missions/mission_file.json')
    return render(request,'controlcenter/boundaryGrid.html',{'mission':mission_file.jsonFile})

def wayPointsGrid(request):
    mission_file = ParseJsonFile(os.getcwd() + '/controlcenter/missions/mission_file.json')
    return render(request,'controlcenter/wayPointsGrid.html',{'mission':mission_file.jsonFile})

def completeMap(request):
    mission_file = ParseJsonFile(os.getcwd() + '/controlcenter/missions/mission_file.json')
    return render(request,'controlcenter/completeMap.html',{'mission':mission_file.jsonFile})

def searchGrid(request):
    mission_file = ParseJsonFile(os.getcwd() + '/controlcenter/missions/mission_file.json')
    return render(request,'controlcenter/searchGrid.html',{'mission':mission_file.jsonFile})
