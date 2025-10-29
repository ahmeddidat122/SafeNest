from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    AutomationRule, SensorReading, VoiceCommand, GestureCommand,
    SafetyProtocol, AutomationLog, DeviceStatus
)
import json
from datetime import datetime, timedelta

@login_required
def automation_dashboard(request):
    """Main automation dashboard"""
    user_rules = AutomationRule.objects.filter(user=request.user, is_active=True)
    recent_logs = AutomationLog.objects.filter(user=request.user)[:10]
    active_devices = DeviceStatus.objects.filter(is_online=True)
    recent_sensors = SensorReading.objects.all()[:10]
    
    context = {
        'title': 'Smart Home Automation',
        'user_rules': user_rules,
        'recent_logs': recent_logs,
        'active_devices': active_devices,
        'recent_sensors': recent_sensors,
        'total_rules': user_rules.count(),
        'online_devices': active_devices.count(),
    }
    return render(request, 'automation/dashboard.html', context)

@login_required
def voice_control(request):
    """Voice control interface"""
    recent_commands = VoiceCommand.objects.filter(user=request.user)[:10]
    
    context = {
        'title': 'Voice Control',
        'recent_commands': recent_commands,
    }
    return render(request, 'automation/voice_control.html', context)

@login_required
def gesture_control(request):
    """Hand gesture control interface"""
    recent_gestures = GestureCommand.objects.filter(user=request.user)[:10]
    
    context = {
        'title': 'Gesture Control',
        'recent_gestures': recent_gestures,
        'gesture_types': GestureCommand.GESTURE_TYPES,
    }
    return render(request, 'automation/gesture_control.html', context)

def safety_monitoring(request):
    """Safety monitoring dashboard"""
    active_protocols = SafetyProtocol.objects.filter(is_active=True)
    recent_alerts = SensorReading.objects.filter(is_alert=True)[:10]
    gas_sensors = SensorReading.objects.filter(sensor_type='gas')[:5]
    fire_sensors = SensorReading.objects.filter(sensor_type='fire')[:5]
    
    context = {
        'title': 'Safety Monitoring',
        'active_protocols': active_protocols,
        'recent_alerts': recent_alerts,
        'gas_sensors': gas_sensors,
        'fire_sensors': fire_sensors,
    }
    return render(request, 'automation/safety_monitoring.html', context)

@login_required
def automation_rules(request):
    """Manage automation rules"""
    user_rules = AutomationRule.objects.filter(user=request.user)
    
    context = {
        'title': 'Automation Rules',
        'user_rules': user_rules,
        'trigger_types': AutomationRule.TRIGGER_TYPES,
        'action_types': AutomationRule.ACTION_TYPES,
    }
    return render(request, 'automation/rules.html', context)

@api_view(['POST'])
def process_voice_command(request):
    """Process voice command from frontend"""
    command_text = request.data.get('command', '').lower()
    
    if not command_text:
        return Response({'error': 'No command provided'}, status=400)
    
    # Simple command interpretation (in production, use NLP/AI)
    interpreted_action = 'unknown'
    target_device = ''
    confidence = 0.5
    
    if 'turn on' in command_text and 'light' in command_text:
        interpreted_action = 'turn_on_lights'
        target_device = 'lights'
        confidence = 0.9
    elif 'turn off' in command_text and 'light' in command_text:
        interpreted_action = 'turn_off_lights'
        target_device = 'lights'
        confidence = 0.9
    elif 'temperature' in command_text:
        interpreted_action = 'adjust_temperature'
        target_device = 'thermostat'
        confidence = 0.8
    elif 'security' in command_text:
        interpreted_action = 'check_security'
        target_device = 'security_system'
        confidence = 0.8
    
    # Log the command
    voice_command = VoiceCommand.objects.create(
        user=request.user,
        command_text=command_text,
        interpreted_action=interpreted_action,
        target_device=target_device,
        confidence_score=confidence,
        executed_successfully=confidence > 0.7
    )
    
    # Log automation action
    AutomationLog.objects.create(
        user=request.user,
        log_type='voice_command',
        description=f"Voice command: {command_text}",
        device_id=target_device,
        success=confidence > 0.7,
        metadata={'confidence': confidence, 'action': interpreted_action}
    )
    
    return Response({
        'success': True,
        'interpreted_action': interpreted_action,
        'target_device': target_device,
        'confidence': confidence,
        'executed': confidence > 0.7,
        'response': f"Command '{interpreted_action}' executed on {target_device}" if confidence > 0.7 else "Command not recognized"
    })

@api_view(['POST'])
def process_gesture_command(request):
    """Process hand gesture command"""
    gesture_type = request.data.get('gesture_type')
    
    if not gesture_type:
        return Response({'error': 'No gesture type provided'}, status=400)
    
    # Simple gesture interpretation
    interpreted_action = 'unknown'
    target_device = ''
    confidence = 0.8
    
    gesture_mappings = {
        'swipe_right': ('turn_on_lights', 'lights'),
        'swipe_left': ('turn_off_lights', 'lights'),
        'swipe_up': ('increase_temperature', 'thermostat'),
        'swipe_down': ('decrease_temperature', 'thermostat'),
        'fist': ('lock_doors', 'security_system'),
        'open_palm': ('unlock_doors', 'security_system'),
        'thumbs_up': ('activate_security', 'security_system'),
        'thumbs_down': ('deactivate_security', 'security_system'),
    }
    
    if gesture_type in gesture_mappings:
        interpreted_action, target_device = gesture_mappings[gesture_type]
        confidence = 0.9
    
    # Log the gesture
    gesture_command = GestureCommand.objects.create(
        user=request.user,
        gesture_type=gesture_type,
        interpreted_action=interpreted_action,
        target_device=target_device,
        confidence_score=confidence,
        executed_successfully=confidence > 0.7
    )
    
    # Log automation action
    AutomationLog.objects.create(
        user=request.user,
        log_type='gesture_command',
        description=f"Gesture command: {gesture_type}",
        device_id=target_device,
        success=confidence > 0.7,
        metadata={'confidence': confidence, 'action': interpreted_action}
    )
    
    return Response({
        'success': True,
        'interpreted_action': interpreted_action,
        'target_device': target_device,
        'confidence': confidence,
        'executed': confidence > 0.7
    })

@api_view(['POST'])
def sensor_data_webhook(request):
    """Webhook for receiving sensor data from IoT devices"""
    device_id = request.data.get('device_id')
    sensor_type = request.data.get('sensor_type')
    value = request.data.get('value')
    unit = request.data.get('unit', '')
    location = request.data.get('location', '')
    
    if not all([device_id, sensor_type, value is not None]):
        return Response({'error': 'Missing required fields'}, status=400)
    
    # Determine if this is an alert condition
    is_alert = False
    if sensor_type == 'gas' and float(value) > 50:  # Gas concentration threshold
        is_alert = True
    elif sensor_type == 'fire' and float(value) > 80:  # Fire detection threshold
        is_alert = True
    elif sensor_type == 'smoke' and float(value) > 30:  # Smoke threshold
        is_alert = True
    
    # Create sensor reading
    reading = SensorReading.objects.create(
        device_id=device_id,
        sensor_type=sensor_type,
        value=float(value),
        unit=unit,
        location=location,
        is_alert=is_alert
    )
    
    # If it's an alert, trigger safety protocols
    if is_alert:
        trigger_safety_protocol(sensor_type, float(value), location)
    
    return Response({
        'success': True,
        'reading_id': reading.id,
        'is_alert': is_alert,
        'timestamp': reading.timestamp
    })

def trigger_safety_protocol(sensor_type, value, location):
    """Trigger appropriate safety protocol based on sensor reading"""
    if sensor_type == 'gas':
        # Gas leak detected - turn on exhaust fan
        AutomationLog.objects.create(
            log_type='safety_activated',
            description=f"Gas leak detected ({value}) at {location}. Activating exhaust fan.",
            device_id='exhaust_fan',
            success=True,
            metadata={'sensor_type': sensor_type, 'value': value, 'location': location}
        )
        
        # Update device status
        DeviceStatus.objects.update_or_create(
            device_id='exhaust_fan',
            defaults={
                'device_name': 'Exhaust Fan',
                'device_type': 'fan',
                'is_online': True,
                'current_state': {'status': 'on', 'speed': 'high', 'reason': 'gas_leak_detected'}
            }
        )
    
    elif sensor_type == 'fire':
        # Fire detected - activate water spray system
        AutomationLog.objects.create(
            log_type='safety_activated',
            description=f"Fire detected ({value}) at {location}. Activating water spray system.",
            device_id='water_spray_system',
            success=True,
            metadata={'sensor_type': sensor_type, 'value': value, 'location': location}
        )
        
        # Update device status
        DeviceStatus.objects.update_or_create(
            device_id='water_spray_system',
            defaults={
                'device_name': 'Water Spray System',
                'device_type': 'safety',
                'is_online': True,
                'current_state': {'status': 'active', 'reason': 'fire_detected'}
            }
        )

@api_view(['GET'])
def device_status_api(request):
    """Get current status of all devices"""
    devices = DeviceStatus.objects.all()
    
    device_data = []
    for device in devices:
        device_data.append({
            'device_id': device.device_id,
            'device_name': device.device_name,
            'device_type': device.device_type,
            'is_online': device.is_online,
            'current_state': device.current_state,
            'location': device.location,
            'last_seen': device.last_seen
        })
    
    return Response({
        'devices': device_data,
        'total_devices': len(device_data),
        'online_devices': sum(1 for d in device_data if d['is_online'])
    })

@api_view(['POST'])
def control_device(request):
    """Control a specific device"""
    device_id = request.data.get('device_id')
    action = request.data.get('action')
    parameters = request.data.get('parameters', {})
    
    if not device_id or not action:
        return Response({'error': 'device_id and action are required'}, status=400)
    
    try:
        device = DeviceStatus.objects.get(device_id=device_id)
        
        # Update device state based on action
        new_state = device.current_state.copy()
        
        if action == 'turn_on':
            new_state['status'] = 'on'
        elif action == 'turn_off':
            new_state['status'] = 'off'
        elif action == 'toggle':
            new_state['status'] = 'off' if new_state.get('status') == 'on' else 'on'
        elif action == 'set_value':
            new_state.update(parameters)
        
        device.current_state = new_state
        device.save()
        
        # Log the action
        AutomationLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            log_type='manual_action',
            description=f"Device {device_id} action: {action}",
            device_id=device_id,
            success=True,
            metadata={'action': action, 'parameters': parameters}
        )
        
        return Response({
            'success': True,
            'device_id': device_id,
            'new_state': new_state,
            'message': f"Device {device_id} {action} executed successfully"
        })
        
    except DeviceStatus.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)
