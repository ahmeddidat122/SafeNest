from django.db import models
from core.models import Home

class Device(models.Model):
    DEVICE_TYPES = [
        ('light', 'Smart Light'),
        ('thermostat', 'Thermostat'),
        ('camera', 'Security Camera'),
        ('sensor', 'Sensor'),
        ('lock', 'Smart Lock'),
        ('speaker', 'Smart Speaker'),
    ]
    
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    room = models.CharField(max_length=50)
    is_online = models.BooleanField(default=False)
    status = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)