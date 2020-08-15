from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import InteropServerForm, MainPageForm
from .models import InteropServer
from .connect import connect
from .parseJson import ParseJsonFile
import json
import math
# Create your views here.

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
    #connect("http://localhost:8000","testuser","testpass")
    server = InteropServer.objects.all()[0]
    # sends request to server to mission file
    #connect(server.url,server.username,server.password) 
    mission_file = ParseJsonFile('/home/muniker/Desktop/AUVSI_System/AUVSI_System/controlcenter/text.json')
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


def boundaryGrid(request):
    mission_file = ParseJsonFile('/home/muniker/Desktop/AUVSI_System/AUVSI_System/controlcenter/text.json')
    return render(request,'controlcenter/boundaryGrid.html',{'mission':mission_file.jsonFile})

def wayPointsGrid(request):
    mission_file = ParseJsonFile('/home/muniker/Desktop/AUVSI_System/AUVSI_System/controlcenter/text.json')
    return render(request,'controlcenter/wayPointsGrid.html',{'mission':mission_file.jsonFile})

def completeMap(request):
    mission_file = ParseJsonFile('/home/muniker/Desktop/AUVSI_System/AUVSI_System/controlcenter/text.json')
    return render(request,'controlcenter/completeMap.html',{'mission':mission_file.jsonFile})

def searchGrid(request):
    mission_file = ParseJsonFile('/home/muniker/Desktop/AUVSI_System/AUVSI_System/controlcenter/text.json')
    return render(request,'controlcenter/searchGrid.html',{'mission':mission_file.jsonFile})
