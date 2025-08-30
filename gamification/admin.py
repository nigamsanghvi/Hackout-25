from django.contrib import admin
from .models import Badge, UserBadge, Activity

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'points_required', 'reports_required', 'special_condition']
    list_filter = ['points_required']
    search_fields = ['name', 'description']

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'points_earned', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'description']
    readonly_fields = ['created_at']