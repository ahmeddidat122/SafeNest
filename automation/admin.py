from django.contrib import admin
from .models import (
    AutomationRule, SensorReading, VoiceCommand, GestureCommand,
    SafetyProtocol, AutomationLog, DeviceStatus
)

@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'trigger_type', 'action_type', 'is_active', 'last_triggered']
    list_filter = ['trigger_type', 'action_type', 'is_active']

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'sensor_type', 'value', 'unit', 'is_alert', 'timestamp']
    list_filter = ['sensor_type', 'is_alert', 'timestamp']

@admin.register(VoiceCommand)
class VoiceCommandAdmin(admin.ModelAdmin):
    list_display = ['user', 'command_text', 'interpreted_action', 'confidence_score', 'executed_successfully']
    list_filter = ['executed_successfully', 'timestamp']

@admin.register(GestureCommand)
class GestureCommandAdmin(admin.ModelAdmin):
    list_display = ['user', 'gesture_type', 'interpreted_action', 'confidence_score', 'executed_successfully']
    list_filter = ['gesture_type', 'executed_successfully']

@admin.register(SafetyProtocol)
class SafetyProtocolAdmin(admin.ModelAdmin):
    list_display = ['name', 'protocol_type', 'is_active', 'priority']
    list_filter = ['protocol_type', 'is_active', 'priority']

@admin.register(AutomationLog)
class AutomationLogAdmin(admin.ModelAdmin):
    list_display = ['log_type', 'description', 'device_id', 'success', 'timestamp']
    list_filter = ['log_type', 'success', 'timestamp']

@admin.register(DeviceStatus)
class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'device_name', 'device_type', 'is_online', 'last_seen']
    list_filter = ['device_type', 'is_online']
