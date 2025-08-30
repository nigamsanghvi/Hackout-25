from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import IncidentReport
from .forms import IncidentReportForm
from .ai_validation import validate_image
from users.models import CustomUser
from gamification.utils import award_points, check_badges
import json

class ReportListView(ListView):
    model = IncidentReport
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by incident type if provided
        incident_type = self.request.GET.get('incident_type')
        if incident_type:
            queryset = queryset.filter(incident_type=incident_type)
        
        # Filter by status if provided
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter parameters to context
        context['incident_type_filter'] = self.request.GET.get('incident_type', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context

class ReportDetailView(DetailView):
    model = IncidentReport
    template_name = 'reports/report_detail.html'
    context_object_name = 'report'

@login_required
def report_create(request):
    if request.method == 'POST':
        form = IncidentReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            
            # Get latitude and longitude from form
            report.latitude = form.cleaned_data['latitude']
            report.longitude = form.cleaned_data['longitude']
            
            report.save()
            
            # AI validation (simulated)
            ai_confidence = validate_image(report.photo.path, report.incident_type)
            report.ai_confidence = ai_confidence
            report.save()
            
            # Award points for reporting
            award_points(request.user, 10, "Reported an incident")
            
            # Check for new badges
            check_badges(request.user)
            
            messages.success(request, 'Your report has been submitted successfully!')
            return redirect('report_detail', pk=report.id)
    else:
        form = IncidentReportForm()
    
    return render(request, 'reports/report_form.html', {'form': form})

def report_map(request):
    reports = IncidentReport.objects.all()
    
    context = {
        'reports': reports,
        'total_reports': reports.count(),
        'active_reports': reports.filter(status='reported').count(),
        'under_review': reports.filter(status='under_review').count(),
        'urgent_cases': reports.filter(status='reported').count(),  # You can add an urgency field later
    }
    return render(request, 'reports/report_map.html', context)

@login_required
def validate_report(request, report_id):
    if not request.user.user_type in ['ngo', 'government', 'researcher']:
        messages.error(request, 'You do not have permission to validate reports.')
        return redirect('report_detail', pk=report_id)
    
    report = get_object_or_404(IncidentReport, id=report_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('official_notes', '')
        
        report.status = new_status
        report.official_notes = notes
        report.validated_by = request.user
        report.validated_at = timezone.now()
        report.save()
        
        # Award points to reporter if validated
        if new_status == 'validated':
            award_points(report.reporter, 20, "Report validated")
            check_badges(report.reporter)
        
        messages.success(request, 'Report status updated successfully.')
        return redirect('report_detail', pk=report_id)
    
    return render(request, 'reports/validate_report.html', {'report': report})

# Add this function for the map data API if needed
def report_map_data(request):
    reports = IncidentReport.objects.all()
    
    reports_data = []
    for report in reports:
        reports_data.append({
            'id': str(report.id),
            'incident_type': report.get_incident_type_display(),
            'incident_type_raw': report.incident_type,
            'latitude': report.latitude,
            'longitude': report.longitude,
            'status': report.status,
            'created_at': report.created_at.strftime('%Y-%m-%d'),
            'photo_url': report.photo.url if report.photo else '',
            'description': report.description,
            'location_description': report.location_description or '',
        })
    
    return JsonResponse(reports_data, safe=False)