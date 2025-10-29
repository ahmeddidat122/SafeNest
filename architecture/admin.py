from django.contrib import admin
from .models import (
    ArchitecturalProject, FloorPlan, Room, MaterialEstimate,
    AIGenerationHistory, ProjectShare, ProjectComment
)

@admin.register(ArchitecturalProject)
class ArchitecturalProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'project_type', 'architectural_style', 'is_generated', 'created_at']
    list_filter = ['project_type', 'architectural_style', 'is_generated']
    search_fields = ['name', 'description']

@admin.register(FloorPlan)
class FloorPlanAdmin(admin.ModelAdmin):
    list_display = ['project', 'floor_number', 'name', 'floor_area']
    list_filter = ['floor_number']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'area', 'floor_plan']
    list_filter = ['room_type']

@admin.register(MaterialEstimate)
class MaterialEstimateAdmin(admin.ModelAdmin):
    list_display = ['project', 'total_estimated_cost', 'material_cost', 'labor_cost']

@admin.register(AIGenerationHistory)
class AIGenerationHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'generation_type', 'success', 'generation_time_seconds', 'created_at']
    list_filter = ['generation_type', 'success']

@admin.register(ProjectShare)
class ProjectShareAdmin(admin.ModelAdmin):
    list_display = ['project', 'is_public', 'allow_comments', 'view_count']
    list_filter = ['is_public', 'allow_comments']

@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved']
