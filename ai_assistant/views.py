from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

# Create your views here.

def ai_chat(request):
    """AI chat interface"""
    context = {
        'title': 'AI Assistant - SafeNest',
    }
    return render(request, 'ai_assistant.html', context)

def ai_commands(request):
    """AI commands interface"""
    context = {
        'title': 'AI Commands',
        'available_commands': [
            'Turn on lights',
            'Set temperature',
            'Check security status',
            'Lock doors',
            'Show energy usage'
        ]
    }
    return render(request, 'ai_assistant/commands.html', context)

@api_view(['POST'])
def chat_message(request):
    """Process AI chat message"""
    message = request.data.get('message', '').lower()
    
    # Simple AI responses based on keywords
    responses = {
        'lights': 'I can help you control your lights. Say "turn on lights" or "turn off lights".',
        'temperature': 'The current temperature is 24°C. Would you like me to adjust it?',
        'security': 'Your home security is active. All sensors are functioning normally.',
        'energy': 'Your current energy usage is 156.7 kWh this month.',
        'lock': 'All doors are currently locked and secure.',
        'unlock': 'I can unlock doors for you. Which door would you like to unlock?',
        'help': 'I can help you with lights, temperature, security, energy monitoring, and door locks. What would you like to do?'
    }
    
    response_text = responses.get('help')  # Default response
    for keyword, response in responses.items():
        if keyword in message:
            response_text = response
            break
    
    return Response({
        'response': response_text,
        'timestamp': '2024-01-01T00:00:00Z'
    })

@api_view(['GET'])
def ai_status(request):
    """Get AI assistant status"""
    return Response({
        'status': 'online',
        'version': '1.0.0',
        'capabilities': [
            'voice_recognition',
            'natural_language_processing',
            'device_control',
            'security_monitoring'
        ]
    })
