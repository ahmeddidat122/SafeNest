from django.contrib import admin
from .models import (
    MaterialCategory, Material, Supplier, SupplierMaterial,
    ProjectEstimate, EstimateItem, PriceHistory, MaterialCalculator
)

@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit', 'current_price', 'is_available']
    list_filter = ['category', 'unit', 'is_available']
    search_fields = ['name', 'brand']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'rating', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active']

@admin.register(ProjectEstimate)
class ProjectEstimateAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'project_type', 'total_cost', 'is_finalized']
    list_filter = ['project_type', 'is_finalized']
