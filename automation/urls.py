from django.urls import path
from . import views

app_name = 'automation'

urlpatterns = [
    path('', views.automation_dashboard, name='dashboard'),
    path('voice/', views.voice_control, name='voice_control'),
    path('gesture/', views.gesture_control, name='gesture_control'),
    path('safety/', views.safety_monitoring, name='safety_monitoring'),
    path('rules/', views.automation_rules, name='rules'),
    
    # API endpoints
    path('api/voice-command/', views.process_voice_command, name='api_voice_command'),
    path('api/gesture-command/', views.process_gesture_command, name='api_gesture_command'),
    path('api/sensor-data/', views.sensor_data_webhook, name='api_sensor_data'),
    path('api/device-status/', views.device_status_api, name='api_device_status'),
    path('api/control-device/', views.control_device, name='api_control_device'),
]
