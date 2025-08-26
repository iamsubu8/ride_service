from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('create_ride/', CreateRideView.as_view(), name='create_ride'),
    path('ride/<int:ride_id>/update_status/', RideStatusUpdateView.as_view(), name='ride_status_update'),
]