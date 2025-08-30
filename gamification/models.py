from django.db import models
from users.models import CustomUser
from django.utils import timezone

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="CSS class for the badge icon")
    points_required = models.IntegerField(default=0)
    reports_required = models.IntegerField(default=0)
    special_condition = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'badge']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)
    points_earned = models.IntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"