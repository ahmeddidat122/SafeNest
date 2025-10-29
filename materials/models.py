from django.db import models
from django.contrib.auth.models import User

class MaterialCategory(models.Model):
    """Categories for construction materials"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class")
    
    class Meta:
        verbose_name_plural = "Material Categories"
    
    def __str__(self):
        return self.name

class Material(models.Model):
    """Construction materials database"""
    UNIT_CHOICES = [
        ('sqft', 'Square Feet'),
        ('cuft', 'Cubic Feet'),
        ('cuyd', 'Cubic Yards'),
        ('lnft', 'Linear Feet'),
        ('bdft', 'Board Feet'),
        ('ton', 'Tons'),
        ('lb', 'Pounds'),
        ('kg', 'Kilograms'),
        ('piece', 'Pieces'),
        ('gallon', 'Gallons'),
        ('liter', 'Liters'),
        ('bag', 'Bags'),
        ('roll', 'Rolls'),
    ]
    
    category = models.ForeignKey(MaterialCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Specifications
    brand = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    specifications = models.JSONField(default=dict, help_text="Technical specifications")
    
    # Availability
    is_available = models.BooleanField(default=True)
    lead_time_days = models.IntegerField(default=0, help_text="Lead time in days")
    minimum_order = models.FloatField(default=1.0, help_text="Minimum order quantity")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.unit})"

class Supplier(models.Model):
    """Material suppliers"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    # Business Info
    business_license = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Rating and Reviews
    rating = models.FloatField(default=0.0, help_text="Average rating out of 5")
    total_reviews = models.IntegerField(default=0)
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class SupplierMaterial(models.Model):
    """Materials offered by suppliers"""
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    supplier_price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    lead_time_days = models.IntegerField(default=0)
    minimum_order = models.FloatField(default=1.0)
    
    # Supplier-specific details
    supplier_sku = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['supplier', 'material']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.material.name}"

class ProjectEstimate(models.Model):
    """Material estimates for projects"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Project Details
    project_type = models.CharField(max_length=50, choices=[
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('renovation', 'Renovation'),
        ('addition', 'Addition'),
    ])
    total_area = models.FloatField(help_text="Total area in square feet")
    
    # Cost Summary
    material_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    labor_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    overhead_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Status
    is_finalized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - ${self.total_cost}"

class EstimateItem(models.Model):
    """Individual items in a project estimate"""
    estimate = models.ForeignKey(ProjectEstimate, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Additional details
    notes = models.TextField(blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.material.name} x {self.quantity}"

class PriceHistory(models.Model):
    """Historical pricing data for materials"""
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_recorded']
    
    def __str__(self):
        return f"{self.material.name} - ${self.price} on {self.date_recorded.date()}"

class MaterialCalculator(models.Model):
    """Predefined calculation formulas for materials"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(MaterialCategory, on_delete=models.CASCADE)
    
    # Calculation Formula
    formula = models.TextField(help_text="Python formula for calculation")
    input_parameters = models.JSONField(default=list, help_text="List of required input parameters")
    output_materials = models.JSONField(default=list, help_text="List of materials and quantities")
    
    # Usage
    usage_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserFavorite(models.Model):
    """User's favorite materials"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'material']
    
    def __str__(self):
        return f"{self.user.username} - {self.material.name}"
