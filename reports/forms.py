# reports/forms.py

from django import forms
from .models import IncidentReport

class IncidentReportForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=True)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=True)
    
    class Meta:
        model = IncidentReport
        fields = ['incident_type', 'description', 'location_description', 'photo', 'latitude', 'longitude']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }