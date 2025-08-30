from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('community', 'Community Member'),
        ('fisherman', 'Fisherman'),
        ('scientist', 'Citizen Scientist'),
        ('ngo', 'NGO Staff'),
        ('government', 'Government Official'),
        ('researcher', 'Researcher'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='community')
    phone_number = models.CharField(max_length=15, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
        