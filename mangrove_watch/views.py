from django.shortcuts import render
from django.views.generic import TemplateView
from reports.models import IncidentReport
from users.models import CustomUser
from mangrovearea.models import MangroveArea
from django.http import JsonResponse

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_reports'] = IncidentReport.objects.all().order_by('-created_at')[:6]
        context['top_users'] = CustomUser.objects.order_by('-points')[:5]
        context['total_reports'] = IncidentReport.objects.count()
        context['validated_reports'] = IncidentReport.objects.filter(status='validated').count()
        context['active_users'] = CustomUser.objects.count()
        context['protected_areas'] = 25  # You can make this dynamic later
        
        # Calculate validation rate
        if context['total_reports'] > 0:
            context['validation_rate'] = (context['validated_reports'] / context['total_reports']) * 100
        else:
            context['validation_rate'] = 0
            
        return context


# If you need any other project-level views, you can add them here
# For example, an about page or contact page

def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def mangrove_areas_api(request):
    """API to fetch mangrove areas as JSON for the map"""
    areas = MangroveArea.objects.filter(is_active=True)
    data = []
    
    for area in areas:
        data.append({
            'aid': area.aid,
            'name': area.name,
            'state': area.state,
            'latitude': float(area.latitude),
            'longitude': float(area.longitude),
            'threat_level': area.threat_level,
            'area_size': area.area_size,
            'description': area.description,
            'created_at': area.created_at.strftime('%b %d, %Y')
        })
    
    return JsonResponse({'mangrove_areas': data})
