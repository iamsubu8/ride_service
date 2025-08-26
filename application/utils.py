import math
from .models import *
from django.db.models import Q
from django.utils import timezone

def distance_calculate(lat1, lon1, lat2, lon2):
    """it calculates the distance bitween to co-ordinates"""
    try:
        R = 6371  
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c
        return round(distance,2)
    except Exception as e:
        return str(e)

def allocate_drivers():
    try:
        """
        this function run while create ride api calls and it assign available drivers to rides.
        """
        rides = Ride.objects.filter(status='create_ride', driver__isnull=True)
        for ride in rides:
            search_radius = 2
            max_radius = 10
            found_driver = None
            while search_radius <= max_radius and not found_driver:
                drivers = Driver.objects.filter(
                    status='available',
                    active_ride__isnull=True
                )
                thirty_mins_ago = timezone.now() - timezone.timedelta(minutes=30)
                drivers = drivers.exclude(
                    rides__rider=ride.rider,
                    rides__status='end_ride',
                    rides__end_time__gte=thirty_mins_ago
                )
                for driver in drivers:
                    last_histories = DriverHistory.objects.filter(driver=driver).order_by('-timestamp')[:2]
                    if last_histories.count() == 2 and all(h.status == 'cancelled' for h in last_histories):
                        continue
                    dist = distance_calculate(driver.latitude, driver.longitude, ride.pickup_lat, ride.pickup_lng)
                    if dist <= search_radius:
                        found_driver = driver
                        break
                search_radius += 2
            if found_driver:
                ride.driver = found_driver
                ride.status = 'driver_assigned'
                ride.driver_assigned_at = timezone.now()
                ride.save()
                found_driver.status = 'busy'
                found_driver.active_ride = ride
                found_driver.save()
    except Exception as e:
        return str(e)

def compute_fare(ride):
    try:
        base_fare = PriceConfig.objects.get(key='base_fare').value
        price_per_km = PriceConfig.objects.get(key='price_per_km').value
        price_per_min = PriceConfig.objects.get(key='price_per_min').value
        waiting_charge = PriceConfig.objects.get(key='waiting_charge').value
        distance = distance_calculate(ride.pickup_lat, ride.pickup_lng, ride.drop_lat, ride.drop_lng)
        # print(distance)
        if ride.start_time and ride.end_time:
            duration = (ride.end_time - ride.start_time).total_seconds() / 60
            # print(duration)
        else:
            duration = 0
        if ride.driver_at_location_at and ride.start_time:
            waiting_time = (ride.start_time - ride.driver_at_location_at).total_seconds() / 60
        else:
            waiting_time = 0

        fare = base_fare + (distance * price_per_km) + (duration * price_per_min) + (waiting_time * waiting_charge)
        ride.fare_amount = fare
        ride.save()
        # print(fare)
        return fare
    except Exception as e:
        return str(e)