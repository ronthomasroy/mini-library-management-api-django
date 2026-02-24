"""
URL configuration for library_project project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
    # Enables login/logout links in the DRF browsable API
    path('api-auth/', include('rest_framework.urls')),
]
