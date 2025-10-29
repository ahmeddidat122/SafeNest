from django.db import models
from django.contrib.auth.models import User
import json

class ArchitecturalProject(models.Model):
    """AI-generated architectural projects"""
    PROJECT_TYPES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('mixed_use', 'Mixed Use'),
    ]
    
    STYLE_TYPES = [
        ('modern', 'Modern'),
        ('contemporary', 'Contemporary'),
        ('traditional', 'Traditional'),
        ('minimalist', 'Minimalist'),
        ('colonial', 'Colonial'),
        ('victorian', 'Victorian'),
        ('mediterranean', 'Mediterranean'),
        ('industrial', 'Industrial'),
        ('rustic', 'Rustic'),
        ('art_deco', 'Art Deco'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    architectural_style = models.CharField(max_length=20, choices=STYLE_TYPES)
    
    # AI Generation Parameters
    ai_prompt = models.TextField(help_text="Original text prompt for AI generation")
    generated_model_url = models.URLField(blank=True, help_text="URL to 3D model file")
    generated_images = models.JSONField(default=list, help_text="List of generated image URLs")
    
    # Project Specifications
    total_area = models.FloatField(null=True, blank=True, help_text="Total area in square feet")
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    floors = models.IntegerField(default=1)
    garage_spaces = models.IntegerField(default=0)
    
    # Location and Environment
    location = models.CharField(max_length=200, blank=True)
    climate_zone = models.CharField(max_length=50, blank=True)
    lot_size = models.FloatField(null=True, blank=True, help_text="Lot size in square feet")
    
    # Generation Status
    is_generated = models.BooleanField(default=False)
    generation_status = models.CharField(max_length=50, default='pending')
    generation_progress = models.IntegerField(default=0, help_text="Progress percentage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.project_type})"

class FloorPlan(models.Model):
    """Floor plans for architectural projects"""
    project = models.ForeignKey(ArchitecturalProject, on_delete=models.CASCADE, related_name='floor_plans')
    floor_number = models.IntegerField(default=1)
    name = models.CharField(max_length=100, help_text="e.g., Ground Floor, First Floor")
    
    # Floor Specifications
    floor_area = models.FloatField(help_text="Floor area in square feet")
    ceiling_height = models.FloatField(default=9.0, help_text="Ceiling height in feet")
    
    # Generated Content
    floor_plan_image = models.URLField(blank=True, help_text="URL to floor plan image")
    room_layout = models.JSONField(default=dict, help_text="Room layout data")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['floor_number']
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"

class Room(models.Model):
    """Individual rooms in floor plans"""
    ROOM_TYPES = [
        ('living_room', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('bathroom', 'Bathroom'),
        ('kitchen', 'Kitchen'),
        ('dining_room', 'Dining Room'),
        ('office', 'Office'),
        ('garage', 'Garage'),
        ('basement', 'Basement'),
        ('attic', 'Attic'),
        ('laundry', 'Laundry Room'),
        ('pantry', 'Pantry'),
        ('closet', 'Closet'),
        ('hallway', 'Hallway'),
        ('balcony', 'Balcony'),
        ('porch', 'Porch'),
        ('other', 'Other'),
    ]
    
    floor_plan = models.ForeignKey(FloorPlan, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    area = models.FloatField(help_text="Room area in square feet")
    
    # Room Position and Dimensions
    x_position = models.FloatField(default=0.0)
    y_position = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    
    # Room Features
    windows = models.IntegerField(default=0)
    doors = models.IntegerField(default=1)
    electrical_outlets = models.IntegerField(default=2)
    special_features = models.JSONField(default=list, help_text="List of special features")
    
    def __str__(self):
        return f"{self.name} ({self.room_type})"

class MaterialEstimate(models.Model):
    """Material estimates for architectural projects"""
    project = models.ForeignKey(ArchitecturalProject, on_delete=models.CASCADE, related_name='material_estimates')
    
    # Structural Materials
    concrete_cubic_yards = models.FloatField(default=0.0)
    steel_tons = models.FloatField(default=0.0)
    lumber_board_feet = models.FloatField(default=0.0)
    bricks_count = models.IntegerField(default=0)
    
    # Finishing Materials
    flooring_sqft = models.FloatField(default=0.0)
    paint_gallons = models.FloatField(default=0.0)
    roofing_sqft = models.FloatField(default=0.0)
    windows_count = models.IntegerField(default=0)
    doors_count = models.IntegerField(default=0)
    
    # Electrical and Plumbing
    electrical_fixtures = models.IntegerField(default=0)
    plumbing_fixtures = models.IntegerField(default=0)
    hvac_units = models.IntegerField(default=0)
    
    # Cost Estimates
    material_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    labor_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Additional Details
    detailed_breakdown = models.JSONField(default=dict, help_text="Detailed cost breakdown")
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Materials for {self.project.name}"

class AIGenerationHistory(models.Model):
    """History of AI generation requests"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(ArchitecturalProject, on_delete=models.CASCADE, null=True, blank=True)
    
    # Generation Parameters
    prompt = models.TextField()
    generation_type = models.CharField(max_length=50, choices=[
        ('3d_model', '3D Model'),
        ('floor_plan', 'Floor Plan'),
        ('exterior_view', 'Exterior View'),
        ('interior_view', 'Interior View'),
        ('material_estimate', 'Material Estimate'),
    ])
    
    # Generation Results
    success = models.BooleanField(default=False)
    result_data = models.JSONField(default=dict)
    error_message = models.TextField(blank=True)
    
    # Performance Metrics
    generation_time_seconds = models.FloatField(null=True, blank=True)
    model_version = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.generation_type} generation for {self.user.username}"

class ProjectShare(models.Model):
    """Sharing settings for architectural projects"""
    project = models.OneToOneField(ArchitecturalProject, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    share_token = models.CharField(max_length=100, unique=True, blank=True)
    allow_comments = models.BooleanField(default=True)
    allow_downloads = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Share settings for {self.project.name}"

class ProjectComment(models.Model):
    """Comments on shared projects"""
    project = models.ForeignKey(ArchitecturalProject, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(null=True, blank=True, help_text="Rating from 1-5")
    is_approved = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.project.name}"
