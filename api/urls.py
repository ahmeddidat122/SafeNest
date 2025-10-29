from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
# Add your API viewsets here when available
# router.register(r'devices', DeviceViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # API Status endpoints
    path('status/', views.api_status, name='api_status'),
    path('info/', views.api_info, name='api_info'),
    path('test/', views.api_test, name='api_test'),

    # AI Chatbot endpoints
    path('ai/chat/', views.AIChatView.as_view(), name='ai_chat'),

    # Device Control endpoints
    path('devices/lights/toggle-all/', views.toggle_lights, name='toggle_lights'),
    path('devices/thermostat/set/', views.set_temperature, name='set_temperature'),

    # Security endpoints
    path('security/activate/', views.activate_security, name='activate_security'),

    # Consultation endpoints
    path('consultation/submit/', views.submit_consultation, name='submit_consultation'),

    # System Status endpoints
    path('system/status/', views.system_status, name='system_status'),
    path('ai/status/', views.ai_status, name='ai_status'),
]
