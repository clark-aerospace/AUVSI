'''
    AUVSI_System URL Configuration
'''
from django.contrib import admin
from django.urls import path
from controlcenter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.connectionPage,name='connectionPage'),
    path('controlCenter',views.controlCenter,name='controlCenter'),
    path('get_mission',views.getMission,name='mission'),
    path('boundaryGrid',views.boundaryGrid,name='boundaryGrid'),
    path('wayPointsGrid',views.wayPointsGrid,name='wayPointsGrid'),
    path('completeMap',views.completeMap,name='completeMap'),
    path('searchGrid',views.searchGrid,name='searchGrid'),
]
