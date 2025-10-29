from django.contrib import admin
from .models import (
    ArchitectProfile, ArchitectPortfolio, ArchitectReview,
    ArchitectInquiry, ArchitectCertification, ArchitectService
)

@admin.register(ArchitectProfile)
class ArchitectProfileAdmin(admin.ModelAdmin):
    list_display = ['firm_name', 'contact_person', 'city', 'state', 'average_rating', 'is_verified']
    list_filter = ['is_verified', 'is_available', 'state']
    search_fields = ['firm_name', 'contact_person']

@admin.register(ArchitectPortfolio)
class ArchitectPortfolioAdmin(admin.ModelAdmin):
    list_display = ['title', 'architect', 'project_type', 'year_completed', 'is_featured']
    list_filter = ['project_type', 'year_completed', 'is_featured']

@admin.register(ArchitectReview)
class ArchitectReviewAdmin(admin.ModelAdmin):
    list_display = ['architect', 'client_name', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved']

@admin.register(ArchitectInquiry)
class ArchitectInquiryAdmin(admin.ModelAdmin):
    list_display = ['architect', 'client_name', 'inquiry_type', 'status', 'created_at']
    list_filter = ['inquiry_type', 'status']
