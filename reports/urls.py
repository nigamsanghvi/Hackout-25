from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('map/', views.report_map, name='report_map'),
    path('create/', views.report_create, name='report_create'),
    path('<uuid:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('<uuid:report_id>/validate/', views.validate_report, name='validate_report'),
]