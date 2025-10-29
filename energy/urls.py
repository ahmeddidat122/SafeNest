from django.urls import path
from . import views

app_name = 'energy'

urlpatterns = [
    path('', views.energy_dashboard, name='dashboard'),
    path('calculator/', views.energy_calculator, name='calculator'),
    path('tips/', views.energy_tips, name='tips'),
    path('add-appliance/', views.add_appliance, name='add_appliance'),
    path('remove-appliance/<int:appliance_id>/', views.remove_appliance, name='remove_appliance'),
    
    # API endpoints
    path('api/calculate/', views.calculate_consumption, name='api_calculate'),
    path('api/log-reading/', views.log_energy_reading, name='api_log_reading'),
    path('api/stats/', views.energy_stats, name='api_stats'),
]
