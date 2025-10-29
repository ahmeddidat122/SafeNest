from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def device_list(request):
    """List all devices"""
    context = {
        'title': 'Device Management',
        'devices': [],  # Will be populated when Device model is available
    }
    return render(request, 'devices/device_list.html', context)

def device_detail(request, device_id):
    """Device detail view"""
    context = {
        'title': 'Device Details',
        'device_id': device_id,
    }
    return render(request, 'devices/device_detail.html', context)

@api_view(['GET'])
def device_status(request, device_id):
    """Get device status via API"""
    return Response({
        'device_id': device_id,
        'status': 'online',
        'last_seen': '2024-01-01T00:00:00Z'
    })

@api_view(['POST'])
def toggle_device(request, device_id):
    """Toggle device on/off"""
    return Response({
        'device_id': device_id,
        'status': 'toggled',
        'message': 'Device toggled successfully'
    })
