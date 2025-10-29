from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def security_dashboard(request):
    """Security dashboard view"""
    context = {
        'title': 'Security Dashboard',
        'security_status': 'SECURE',
        'alerts': [],  # Will be populated when SecurityAlert model is available
    }
    return render(request, 'security/dashboard.html', context)

def security_alerts(request):
    """Security alerts view"""
    context = {
        'title': 'Security Alerts',
        'alerts': [],  # Will be populated when SecurityAlert model is available
    }
    return render(request, 'security/alerts.html', context)

@api_view(['GET'])
def security_status(request):
    """Get security system status"""
    return Response({
        'status': 'SECURE',
        'armed': True,
        'sensors': {
            'door': 'closed',
            'window': 'closed',
            'motion': 'clear'
        }
    })

@api_view(['POST'])
def arm_security(request):
    """Arm security system"""
    return Response({
        'status': 'ARMED',
        'message': 'Security system armed successfully'
    })

@api_view(['POST'])
def disarm_security(request):
    """Disarm security system"""
    return Response({
        'status': 'DISARMED',
        'message': 'Security system disarmed successfully'
    })
