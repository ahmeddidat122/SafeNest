from django.contrib import admin
from .models import (
    ConsultationSession, ChatMessage, Consultant, ConsultationRequest,
    ConsultationFeedback, ConsultationResource
)

@admin.register(ConsultationSession)
class ConsultationSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'consultant', 'session_type', 'status', 'created_at']
    list_filter = ['session_type', 'status']

@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'hourly_rate', 'average_rating', 'is_available']
    list_filter = ['is_available', 'expertise_areas']

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'consultation_type', 'urgency', 'status', 'created_at']
    list_filter = ['consultation_type', 'urgency', 'status']

@admin.register(ConsultationFeedback)
class ConsultationFeedbackAdmin(admin.ModelAdmin):
    list_display = ['session', 'overall_rating', 'would_recommend', 'created_at']
    list_filter = ['overall_rating', 'would_recommend']
