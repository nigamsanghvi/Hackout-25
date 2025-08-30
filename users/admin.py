from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'points', 'level', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'organization']
    readonly_fields = ['created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('user_type', 'phone_number', 'organization', 'location', 'bio', 'profile_picture', 'points', 'level')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('user_type', 'phone_number', 'organization')
        }),
    )