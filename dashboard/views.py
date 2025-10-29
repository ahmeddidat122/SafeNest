from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def index(request):
    """Main dashboard view - AI-Powered Smart Home & Architecture Platform"""

    # Smart Home IoT Stats
    smart_home_stats = {
        'active_devices': 12,  # Simulated data
        'avg_temperature': 24.5,
        'energy_usage': 156.7,
        'security_status': 'SECURE',
        'automation_rules': 8,
        'recent_alerts': 2,
    }

    # AI Architecture Stats
    architecture_stats = {
        'total_projects': 45,
        'ai_generations': 128,
        'featured_architects': 23,
        'material_estimates': 67,
        'consultation_sessions': 34,
    }

    # Recent Activity (simulated)
    recent_activity = [
        {'type': 'ai_generation', 'description': 'AI generated 3D model for "Modern Villa"', 'time': '2 hours ago'},
        {'type': 'automation', 'description': 'Gas leak detected - Exhaust fan activated', 'time': '4 hours ago'},
        {'type': 'consultation', 'description': 'Live consultation with John Smith completed', 'time': '6 hours ago'},
        {'type': 'energy', 'description': 'Monthly energy report generated', 'time': '1 day ago'},
        {'type': 'security', 'description': 'Security system armed automatically', 'time': '1 day ago'},
    ]

    # Featured Services
    featured_services = [
        {
            'name': 'AI Architecture Generator',
            'description': 'Generate 3D architectural models from text prompts',
            'icon': 'fas fa-cube',
            'url': '/architecture/generator/',
            'color': 'primary'
        },
        {
            'name': 'Smart Home Automation',
            'description': 'Voice & gesture control for your smart devices',
            'icon': 'fas fa-home',
            'url': '/automation/',
            'color': 'success'
        },
        {
            'name': 'Energy Calculator',
            'description': 'Calculate and optimize your energy consumption',
            'icon': 'fas fa-bolt',
            'url': '/energy/calculator/',
            'color': 'warning'
        },
        {
            'name': 'Material Estimation',
            'description': 'AI-powered material and cost estimation',
            'icon': 'fas fa-calculator',
            'url': '/materials/calculator/',
            'color': 'info'
        },
        {
            'name': 'Find Architects',
            'description': 'Connect with local professional architects',
            'icon': 'fas fa-users',
            'url': '/architects/',
            'color': 'secondary'
        },
        {
            'name': 'Live Consultation',
            'description': 'Get expert advice through live chat',
            'icon': 'fas fa-comments',
            'url': '/consultation/',
            'color': 'danger'
        }
    ]

    context = {
        'title': 'SafeNest - AI-Powered Smart Home & Architecture Platform',
        'smart_home_stats': smart_home_stats,
        'architecture_stats': architecture_stats,
        'recent_activity': recent_activity,
        'featured_services': featured_services,
    }
    return render(request, 'dashboard/index.html', context)

def dashboard_view(request):
    context = {
        'active_devices': 0,  # Device.objects.filter(is_online=True).count() when model is available
        'avg_temperature': 24,  # Calculate from sensors
        'energy_usage': 156.7,  # Calculate from smart meters
    }
    return render(request, 'dashboard/index.html', context)

@api_view(['POST'])
def toggle_lights(request):
    # lights = Device.objects.filter(device_type='light') # Uncomment when Device model is available
    # for light in lights:
    #     current_status = light.status.get('on', False)
    #     light.status['on'] = not current_status
    #     light.save()
    
    # Send real-time update
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'dashboard',
        {
            'type': 'device_update',
            'message': 'Lights toggled'
        }
    )
    
    return Response({'status': 'success'})

@api_view(['POST'])
def ai_chat(request):
    message = request.data.get('message')
    
    # Simple AI responses (integrate with actual AI service)
    responses = {
        'temperature': 'The current temperature is 24°C. Would you like me to adjust it?',
        'lights': 'I can control your lights. Say "turn on lights" or "turn off lights".',
        'security': 'Your home security is active. All sensors are functioning normally.',
        'default': 'I\'m here to help with your smart home. Try asking about temperature, lights, or security.'
    }
    
    response_text = responses.get('default')
    for key, value in responses.items():
        if key in message.lower():
            response_text = value
            break
    
    return Response({'response': response_text})

def demo_view(request):
    """Demo page view"""
    return render(request, 'demo.html')