from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Rider, Ride
from .utils import *

class CreateRideView(APIView):
    def post(self, request):
        """
        This API is for create rides by requesting pickup and drop locations and rider ID.
        """
        try:
            pickup_longitude = request.data.get("pickup_longitude")
            pickup_latitude = request.data.get("pickup_latitude")
            drop_longitude = request.data.get("drop_longitude")
            drop_latitude = request.data.get("drop_latitude")
            rider_id = request.data.get("rider_id")

            if not pickup_longitude or not pickup_latitude:
                return Response({"message": "Pickup Longitude and Latitude Are Required!"}, status=status.HTTP_400_BAD_REQUEST)

            if not drop_longitude or not drop_latitude:
                return Response({"message": "Drop Longitude and Latitude Are Required!"}, status=status.HTTP_400_BAD_REQUEST)

            if not rider_id:
                return Response({"message": "Rider ID Is Required!"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                rider = Rider.objects.get(pk=rider_id)
            except Rider.DoesNotExist:
                return Response({"message": "Rider Not Found!"}, status=status.HTTP_404_NOT_FOUND)

            distance = distance_calculate(float(pickup_latitude), float(pickup_longitude), float(drop_latitude), float(drop_longitude))

            ride = Ride.objects.create(
                rider=rider,
                pickup_lat=pickup_latitude,
                pickup_lng=pickup_longitude,
                drop_lat=drop_latitude,
                drop_lng=drop_longitude,
                status='create_ride'
            )

            return Response({
                "message": "Ride created",
                "ride_id": ride.ride_id,
                "distance": f"{distance} KM"
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RideStatusUpdateView(APIView):
    def post(self, request, ride_id):
        """
        This API is for updating the status of a ride by giving ride id.
        """
        try:
            status_update = request.data.get("status")
            ride = Ride.objects.get(pk=ride_id)

            if status_update == "driver_at_location":
                ride.status = "driver_at_location"
                ride.driver_at_location_at = timezone.now()
            elif status_update == "start_ride":
                ride.status = "start_ride"
                ride.start_time = timezone.now()
            elif status_update == "end_ride":
                ride.status = "end_ride"
                ride.end_time = timezone.now()
                fare = compute_fare(ride)
            else:
                return Response({"message": "Invalid Status!"}, status=status.HTTP_400_BAD_REQUEST)

            ride.save()
            response = {"message": f"Ride Status Updated."}
            if status_update == "end_ride":
                response["fare"] = ride.fare_amount

            return Response(response, status=status.HTTP_200_OK)
        except Ride.DoesNotExist:
            return Response({"message": "Ride Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

