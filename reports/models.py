from django.db import models
from django.utils import timezone
import uuid

class IncidentReport(models.Model):
    INCIDENT_TYPES = [
        ('cutting', 'Illegal Cutting'),
        ('dumping', 'Pollution/Dumping'),
        ('reclamation', 'Land Reclamation'),
        ('other', 'Other Threat'),
    ]
    
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('under_review', 'Under Review'),
        ('validated', 'Validated'),
        ('action_taken', 'Action Taken'),
        ('resolved', 'Resolved'),
        ('false_report', 'False Report'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='reports')
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPES)
    description = models.TextField()
    
    # Replace PointField with regular FloatFields
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    location_description = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='report_photos/')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Validation fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    ai_confidence = models.FloatField(null=True, blank=True)
    validated_by = models.ForeignKey('users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL, related_name='validated_reports')
    validated_at = models.DateTimeField(null=True, blank=True)
    official_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_incident_type_display()} at {self.location_description}"
    
    class Meta:
        ordering = ['-created_at']