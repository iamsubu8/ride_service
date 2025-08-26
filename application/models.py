from django.db import models

# Create your models here.

class Rider(models.Model):
    rider_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    active_ride = models.ForeignKey('Ride', null=True, blank=True, on_delete=models.SET_NULL, related_name="active_driver")
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Ride(models.Model):
    STATUS_CHOICES = [
        ('create_ride', 'Created'),
        ('driver_assigned', 'Driver Assigned'),
        ('driver_at_location', 'Driver At Location'),
        ('start_ride', 'Started'),
        ('end_ride', 'Ended'),
        ('cancelled', 'Cancelled'),
    ]
    ride_id = models.AutoField(primary_key=True)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name="rides")
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL, related_name="rides")
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    drop_lat = models.FloatField()
    drop_lng = models.FloatField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='create_ride')
    created_at = models.DateTimeField(auto_now_add=True)
    driver_assigned_at = models.DateTimeField(null=True, blank=True)
    driver_at_location_at = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    fare_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.ride_id} - {self.status}"

class DriverHistory(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ]
    driver_history_id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class PriceConfig(models.Model):
    price_config_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50, unique=True)
    value = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.value}"
