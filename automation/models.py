from django.db import models
from django.contrib.auth.models import User
import json

class AutomationRule(models.Model):
    """Automation rules for smart home devices"""
    TRIGGER_TYPES = [
        ('sensor', 'Sensor Reading'),
        ('time', 'Time-based'),
        ('voice', 'Voice Command'),
        ('gesture', 'Hand Gesture'),
        ('manual', 'Manual Trigger'),
    ]
    
    ACTION_TYPES = [
        ('turn_on', 'Turn On'),
        ('turn_off', 'Turn Off'),
        ('toggle', 'Toggle'),
        ('set_value', 'Set Value'),
        ('send_notification', 'Send Notification'),
        ('activate_safety', 'Activate Safety Protocol'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_TYPES)
    trigger_conditions = models.JSONField(default=dict, help_text="JSON conditions for trigger")
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_parameters = models.JSONField(default=dict, help_text="JSON parameters for action")
    target_device = models.CharField(max_length=100, help_text="Device ID or type")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_triggered = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.trigger_type} -> {self.action_type})"

class SensorReading(models.Model):
    """Sensor readings from IoT devices"""
    SENSOR_TYPES = [
        ('gas', 'Gas Sensor'),
        ('fire', 'Fire/IR Sensor'),
        ('temperature', 'Temperature Sensor'),
        ('humidity', 'Humidity Sensor'),
        ('motion', 'Motion Sensor'),
        ('door', 'Door Sensor'),
        ('window', 'Window Sensor'),
        ('smoke', 'Smoke Detector'),
        ('water', 'Water Level Sensor'),
        ('light', 'Light Sensor'),
    ]
    
    device_id = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    value = models.FloatField()
    unit = models.CharField(max_length=20, default='')
    location = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_alert = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.sensor_type} reading: {self.value} {self.unit}"

class VoiceCommand(models.Model):
    """Voice commands for smart home control"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    command_text = models.TextField()
    interpreted_action = models.CharField(max_length=100)
    target_device = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(default=0.0)
    executed_successfully = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Voice: '{self.command_text}' -> {self.interpreted_action}"

class GestureCommand(models.Model):
    """Hand gesture commands for smart home control"""
    GESTURE_TYPES = [
        ('swipe_left', 'Swipe Left'),
        ('swipe_right', 'Swipe Right'),
        ('swipe_up', 'Swipe Up'),
        ('swipe_down', 'Swipe Down'),
        ('fist', 'Closed Fist'),
        ('open_palm', 'Open Palm'),
        ('thumbs_up', 'Thumbs Up'),
        ('thumbs_down', 'Thumbs Down'),
        ('peace_sign', 'Peace Sign'),
        ('point', 'Pointing'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gesture_type = models.CharField(max_length=20, choices=GESTURE_TYPES)
    interpreted_action = models.CharField(max_length=100)
    target_device = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(default=0.0)
    executed_successfully = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Gesture: {self.gesture_type} -> {self.interpreted_action}"

class SafetyProtocol(models.Model):
    """Safety automation protocols"""
    PROTOCOL_TYPES = [
        ('gas_leak', 'Gas Leak Detection'),
        ('fire_detection', 'Fire Detection'),
        ('smoke_detection', 'Smoke Detection'),
        ('water_leak', 'Water Leak Detection'),
        ('intrusion', 'Intrusion Detection'),
        ('emergency', 'Emergency Protocol'),
    ]
    
    name = models.CharField(max_length=100)
    protocol_type = models.CharField(max_length=20, choices=PROTOCOL_TYPES)
    trigger_conditions = models.JSONField(default=dict)
    safety_actions = models.JSONField(default=list, help_text="List of safety actions to execute")
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1, help_text="1=Highest, 5=Lowest")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.protocol_type})"

class AutomationLog(models.Model):
    """Log of automation executions"""
    LOG_TYPES = [
        ('rule_triggered', 'Rule Triggered'),
        ('safety_activated', 'Safety Protocol Activated'),
        ('voice_command', 'Voice Command Executed'),
        ('gesture_command', 'Gesture Command Executed'),
        ('manual_action', 'Manual Action'),
        ('error', 'Error Occurred'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    description = models.TextField()
    device_id = models.CharField(max_length=100, blank=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.log_type}: {self.description[:50]}"

class DeviceStatus(models.Model):
    """Current status of smart home devices"""
    device_id = models.CharField(max_length=100, unique=True)
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    is_online = models.BooleanField(default=False)
    current_state = models.JSONField(default=dict, help_text="Current device state/settings")
    location = models.CharField(max_length=100, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    firmware_version = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.device_name} ({self.device_id})"
