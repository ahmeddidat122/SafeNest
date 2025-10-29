from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('admin', 'Admin')
    ])
    phone = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

class Home(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='homes')
    created_at = models.DateTimeField(auto_now_add=True)