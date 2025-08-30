from .admin import admin_site
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView
from mangrove_watch import views

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', HomeView.as_view(), name='home'),
    path('reports/', include('reports.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/mangrove-areas/', views.mangrove_areas_api, name="mangrove_areas_api"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)