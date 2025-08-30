from django.contrib import admin
from .models import IncidentReport

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'incident_type', 'reporter', 'status', 'created_at', 'ai_confidence']
    list_filter = ['incident_type', 'status', 'created_at']
    search_fields = ['description', 'location_description', 'reporter__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'reporter', 'incident_type', 'description')
        }),
        ('Location Details', {
            'fields': ('latitude', 'longitude', 'location_description')
        }),
        ('Evidence', {
            'fields': ('photo',)
        }),
        ('Validation', {
            'fields': ('status', 'ai_confidence', 'validated_by', 'validated_at', 'official_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )