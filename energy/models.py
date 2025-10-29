from django.db import models
from django.contrib.auth.models import User

class Appliance(models.Model):
    """Model for household appliances"""
    APPLIANCE_TYPES = [
        ('refrigerator', 'Refrigerator'),
        ('air_conditioner', 'Air Conditioner'),
        ('washing_machine', 'Washing Machine'),
        ('television', 'Television'),
        ('microwave', 'Microwave'),
        ('dishwasher', 'Dishwasher'),
        ('water_heater', 'Water Heater'),
        ('lighting', 'Lighting'),
        ('computer', 'Computer'),
        ('fan', 'Fan'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    appliance_type = models.CharField(max_length=50, choices=APPLIANCE_TYPES)
    power_rating = models.FloatField(help_text="Power consumption in watts")
    hours_per_day = models.FloatField(default=8.0, help_text="Average hours used per day")
    energy_star_rating = models.IntegerField(null=True, blank=True, help_text="Energy efficiency rating (1-5)")
    purchase_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.appliance_type})"
    
    @property
    def daily_consumption_kwh(self):
        """Calculate daily energy consumption in kWh"""
        return (self.power_rating * self.hours_per_day) / 1000
    
    @property
    def monthly_consumption_kwh(self):
        """Calculate monthly energy consumption in kWh"""
        return self.daily_consumption_kwh * 30
    
    @property
    def monthly_cost(self):
        """Calculate monthly cost (assuming $0.12 per kWh)"""
        return self.monthly_consumption_kwh * 0.12

class UserEnergyProfile(models.Model):
    """User's energy consumption profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    appliances = models.ManyToManyField(Appliance, blank=True)
    electricity_rate = models.FloatField(default=0.12, help_text="Cost per kWh in USD")
    house_size = models.IntegerField(null=True, blank=True, help_text="House size in square feet")
    occupants = models.IntegerField(default=1, help_text="Number of people in household")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Energy Profile"
    
    @property
    def total_monthly_consumption(self):
        """Calculate total monthly consumption for all appliances"""
        return sum(appliance.monthly_consumption_kwh for appliance in self.appliances.all())
    
    @property
    def estimated_monthly_bill(self):
        """Calculate estimated monthly electricity bill"""
        return self.total_monthly_consumption * self.electricity_rate

class EnergyReading(models.Model):
    """Real-time energy readings from IoT devices"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=100)
    power_consumption = models.FloatField(help_text="Current power consumption in watts")
    voltage = models.FloatField(null=True, blank=True)
    current = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Reading for {self.device_id} at {self.timestamp}"

class EnergyTip(models.Model):
    """Energy saving tips and recommendations"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('heating', 'Heating & Cooling'),
        ('lighting', 'Lighting'),
        ('appliances', 'Appliances'),
        ('insulation', 'Insulation'),
        ('general', 'General'),
    ])
    potential_savings = models.CharField(max_length=100, help_text="e.g., '10-15% reduction'")
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
