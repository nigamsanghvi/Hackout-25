from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class MangroveArea(models.Model):
    aid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=6,
        validators=[
            MinValueValidator(-90.0),
            MaxValueValidator(90.0)
        ]
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=6,
        validators=[
            MinValueValidator(-180.0),
            MaxValueValidator(180.0)
        ]
    )
    area_size = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)
    threat_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Risk'),
            ('medium', 'Medium Risk'),
            ('high', 'High Risk'),
            ('critical', 'Critical')
        ],
        default='low'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.state})'
