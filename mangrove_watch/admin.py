from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.response import TemplateResponse
from reports.models import IncidentReport
from users.models import CustomUser
from gamification.models import Badge, UserBadge, Activity
from django.db.models import Count, Sum, Avg, Q
from datetime import datetime, timedelta

# Custom Admin Site Class
class CustomAdminSite(admin.AdminSite):
    site_header = "Community Mangrove Watch Administration"
    site_title = "Mangrove Watch Admin"
    index_title = "Welcome to Mangrove Watch Administration"
    
    def index(self, request, extra_context=None):
        """
        Override the default admin index page to redirect to our custom dashboard
        """
        # Redirect to custom dashboard instead of showing default index
        return HttpResponseRedirect(reverse('custom_admin:dashboard'))
    
    def dashboard(self, request, extra_context=None):
        """
        Custom dashboard view - the new admin homepage
        """
        # Calculate statistics for the dashboard
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        extra_context = extra_context or {}
        extra_context.update({
            'reports_count': IncidentReport.objects.count(),
            'users_count': CustomUser.objects.count(),
            'validated_reports': IncidentReport.objects.filter(status='validated').count(),
            'active_users': CustomUser.objects.filter(
                last_login__gte=thirty_days_ago
            ).count(),
            'total_points': CustomUser.objects.aggregate(Sum('points'))['points__sum'] or 0,
            'recent_reports': IncidentReport.objects.select_related('reporter')
                                  .order_by('-created_at')[:10],
            'user_stats': CustomUser.objects.values('user_type')
                             .annotate(count=Count('id'),
                                      active_count=Count('id', filter=Q(is_active=True)),
                                      total_points=Sum('points'))[:10],
            'reports_by_type': IncidentReport.objects.values('incident_type')
                                  .annotate(count=Count('id'),
                                           validated_count=Count('id', filter=Q(status='validated'))),
        })
        
        # Render the custom dashboard template
        return TemplateResponse(request, 'admin/dashboard.html', extra_context)
    
    def custom_stats(self, request, extra_context=None):
        """
        Additional detailed statistics view
        """
        extra_context = extra_context or {}
        
        # Add more detailed statistics here
        extra_context.update({
            'title': 'Detailed Statistics',
            'reports_count': IncidentReport.objects.count(),
            'users_count': CustomUser.objects.count(),
            # Add more stats as needed
        })
        
        return TemplateResponse(request, 'admin/custom_stats.html', extra_context)
    
    def get_urls(self):
        """
        Register custom URLs including our dashboard
        """
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard), name='dashboard'),
            path('custom-stats/', self.admin_view(self.custom_stats), name='custom_stats'),
        ]
        return custom_urls + urls

# Create and configure the custom admin site
admin_site = CustomAdminSite(name='custom_admin')

# Register your models with the custom admin site
# Reports models
from reports.models import IncidentReport
from reports.admin import IncidentReportAdmin
admin_site.register(IncidentReport, IncidentReportAdmin)

# Users models  
from users.models import CustomUser
from users.admin import CustomUserAdmin
admin_site.register(CustomUser, CustomUserAdmin)

# Gamification models
from gamification.models import Badge, UserBadge, Activity
from gamification.admin import BadgeAdmin, UserBadgeAdmin, ActivityAdmin
admin_site.register(Badge, BadgeAdmin)
admin_site.register(UserBadge, UserBadgeAdmin)
admin_site.register(Activity, ActivityAdmin)

# Replace the default admin site
admin.site = admin_site