from django.contrib import admin
from .models import Appliance, UserEnergyProfile, EnergyReading, EnergyTip

@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = ['name', 'appliance_type', 'power_rating', 'hours_per_day', 'monthly_cost']
    list_filter = ['appliance_type', 'energy_star_rating']
    search_fields = ['name', 'appliance_type']

@admin.register(UserEnergyProfile)
class UserEnergyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'electricity_rate', 'house_size', 'occupants', 'total_monthly_consumption']
    list_filter = ['occupants', 'house_size']

@admin.register(EnergyReading)
class EnergyReadingAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_id', 'power_consumption', 'timestamp']
    list_filter = ['timestamp', 'user']

@admin.register(EnergyTip)
class EnergyTipAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'potential_savings', 'is_active']
    list_filter = ['category', 'difficulty', 'is_active']
