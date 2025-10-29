from django.db import models
from django.contrib.auth.models import User

class ArchitectProfile(models.Model):
    """Architect professional profiles"""
    SPECIALIZATIONS = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('landscape', 'Landscape'),
        ('interior', 'Interior Design'),
        ('sustainable', 'Sustainable Design'),
        ('historic', 'Historic Preservation'),
        ('urban_planning', 'Urban Planning'),
    ]
    
    # Basic Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firm_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    
    # Address
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='USA')
    
    # Professional Details
    license_number = models.CharField(max_length=100, blank=True)
    years_experience = models.IntegerField(default=0)
    specializations = models.JSONField(default=list, help_text="List of specialization areas")
    
    # Profile
    bio = models.TextField(blank=True)
    profile_image = models.URLField(blank=True)
    portfolio_images = models.JSONField(default=list, help_text="List of portfolio image URLs")
    
    # Services and Pricing
    services_offered = models.JSONField(default=list, help_text="List of services offered")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    project_rate_range = models.CharField(max_length=100, blank=True, help_text="e.g., $5,000 - $50,000")
    
    # Ratings and Reviews
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_projects = models.IntegerField(default=0)
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.firm_name

class ArchitectPortfolio(models.Model):
    """Portfolio projects for architects"""
    architect = models.ForeignKey(ArchitectProfile, on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_type = models.CharField(max_length=50, choices=ArchitectProfile.SPECIALIZATIONS)
    
    # Project Details
    location = models.CharField(max_length=200)
    year_completed = models.IntegerField()
    project_size = models.CharField(max_length=100, blank=True, help_text="e.g., 2,500 sq ft")
    budget_range = models.CharField(max_length=100, blank=True)
    
    # Media
    featured_image = models.URLField()
    additional_images = models.JSONField(default=list)
    video_url = models.URLField(blank=True)
    
    # Recognition
    awards = models.JSONField(default=list, help_text="List of awards received")
    publications = models.JSONField(default=list, help_text="List of publications featured in")
    
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-year_completed', '-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.architect.firm_name}"

class ArchitectReview(models.Model):
    """Reviews for architects"""
    architect = models.ForeignKey(ArchitectProfile, on_delete=models.CASCADE, related_name='reviews')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(blank=True)
    
    # Review Content
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    
    # Project Details
    project_type = models.CharField(max_length=50, blank=True)
    project_duration = models.CharField(max_length=100, blank=True)
    project_budget = models.CharField(max_length=100, blank=True)
    
    # Review Categories
    design_quality = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    communication = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    timeliness = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    budget_adherence = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.architect.firm_name} by {self.client_name}"

class ArchitectInquiry(models.Model):
    """Inquiries sent to architects"""
    INQUIRY_TYPES = [
        ('consultation', 'Initial Consultation'),
        ('design', 'Design Services'),
        ('renovation', 'Renovation Project'),
        ('new_construction', 'New Construction'),
        ('planning', 'Planning & Permits'),
        ('other', 'Other'),
    ]
    
    architect = models.ForeignKey(ArchitectProfile, on_delete=models.CASCADE, related_name='inquiries')
    
    # Client Information
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20, blank=True)
    
    # Project Information
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES)
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    project_location = models.CharField(max_length=200, blank=True)
    estimated_budget = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('responded', 'Responded'),
        ('in_discussion', 'In Discussion'),
        ('proposal_sent', 'Proposal Sent'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ], default='pending')
    
    # Communication
    architect_response = models.TextField(blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Inquiry: {self.project_title} to {self.architect.firm_name}"

class ArchitectCertification(models.Model):
    """Professional certifications for architects"""
    architect = models.ForeignKey(ArchitectProfile, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    certification_number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.certification_name} - {self.architect.firm_name}"

class ArchitectService(models.Model):
    """Services offered by architects"""
    architect = models.ForeignKey(ArchitectProfile, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=200)
    description = models.TextField()
    price_range = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.service_name} - {self.architect.firm_name}"
