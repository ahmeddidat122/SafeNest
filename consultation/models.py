from django.db import models
from django.contrib.auth.models import User

class ConsultationSession(models.Model):
    """Live consultation sessions"""
    SESSION_TYPES = [
        ('architecture', 'Architecture Consultation'),
        ('design', 'Design Consultation'),
        ('materials', 'Materials Consultation'),
        ('energy', 'Energy Efficiency'),
        ('smart_home', 'Smart Home Setup'),
        ('general', 'General Consultation'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Session Details
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_sessions')
    consultant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultant_sessions', null=True, blank=True)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Scheduling
    scheduled_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=30)
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    
    # Status and Pricing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Session Data
    session_notes = models.TextField(blank=True)
    client_rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    client_feedback = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.client.username}"

class ChatMessage(models.Model):
    """Chat messages in consultation sessions"""
    session = models.ForeignKey(ConsultationSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    message_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('system', 'System Message'),
    ], default='text')
    
    # File attachments
    file_url = models.URLField(blank=True)
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.IntegerField(null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"

class Consultant(models.Model):
    """Consultant profiles"""
    EXPERTISE_AREAS = [
        ('architecture', 'Architecture'),
        ('interior_design', 'Interior Design'),
        ('structural', 'Structural Engineering'),
        ('electrical', 'Electrical Systems'),
        ('plumbing', 'Plumbing Systems'),
        ('hvac', 'HVAC Systems'),
        ('smart_home', 'Smart Home Technology'),
        ('energy_efficiency', 'Energy Efficiency'),
        ('sustainable_design', 'Sustainable Design'),
        ('project_management', 'Project Management'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    bio = models.TextField()
    expertise_areas = models.JSONField(default=list, help_text="List of expertise areas")
    
    # Professional Details
    years_experience = models.IntegerField(default=0)
    certifications = models.JSONField(default=list, help_text="List of certifications")
    education = models.TextField(blank=True)
    
    # Availability and Pricing
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    availability_schedule = models.JSONField(default=dict, help_text="Weekly availability schedule")
    
    # Performance Metrics
    average_rating = models.FloatField(default=0.0)
    total_sessions = models.IntegerField(default=0)
    total_hours = models.FloatField(default=0.0)
    
    # Profile
    profile_image = models.URLField(blank=True)
    languages = models.JSONField(default=list, help_text="Languages spoken")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title}"

class ConsultationRequest(models.Model):
    """Requests for consultation"""
    URGENCY_LEVELS = [
        ('low', 'Low - Within a week'),
        ('medium', 'Medium - Within 2-3 days'),
        ('high', 'High - Within 24 hours'),
        ('urgent', 'Urgent - ASAP'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_requests')
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, null=True, blank=True)
    
    # Request Details
    consultation_type = models.CharField(max_length=20, choices=ConsultationSession.SESSION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default='medium')
    
    # Preferences
    preferred_time = models.DateTimeField(null=True, blank=True)
    duration_needed = models.IntegerField(default=30, help_text="Duration in minutes")
    budget_range = models.CharField(max_length=100, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='open')
    
    # Assignment
    assigned_consultant = models.ForeignKey(Consultant, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    session = models.OneToOneField(ConsultationSession, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.client.username}"

class ConsultationFeedback(models.Model):
    """Feedback for consultation sessions"""
    session = models.OneToOneField(ConsultationSession, on_delete=models.CASCADE)
    
    # Ratings
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    consultant_knowledge = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    communication_quality = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    problem_solving = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    value_for_money = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Written Feedback
    what_went_well = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    would_recommend = models.BooleanField(default=True)
    additional_comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.session.title}"

class ConsultationResource(models.Model):
    """Resources shared during consultations"""
    RESOURCE_TYPES = [
        ('document', 'Document'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Web Link'),
        ('template', 'Template'),
        ('checklist', 'Checklist'),
    ]
    
    session = models.ForeignKey(ConsultationSession, on_delete=models.CASCADE, related_name='resources')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    
    # Resource Data
    file_url = models.URLField(blank=True)
    external_link = models.URLField(blank=True)
    content = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.session.title}"
