from django.db import models
from core.models import Home

class SecurityAlert(models.Model):
    ALERT_TYPES = [
        ('fire', 'Fire Detection'),
        ('gas', 'Gas Leak'),
        ('intrusion', 'Intrusion'),
        ('temperature', 'Temperature Alert'),
    ]
    
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)