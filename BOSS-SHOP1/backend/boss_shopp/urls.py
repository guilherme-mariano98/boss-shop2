"""boss_shopp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import JsonResponse
import os

from django.views.static import serve
from django.http import Http404

def serve_frontend(request, path=''):
    """Serve frontend files"""
    frontend_dir = settings.BASE_DIR.parent / 'frontend'
    
    if not path:
        path = 'index.html'
    
    try:
        return serve(request, path, document_root=frontend_dir)
    except Http404:
        # If file not found, serve index.html (for SPA routing)
        return serve(request, 'index.html', document_root=frontend_dir)

def root_view(request):
    """Root endpoint - serve the main website"""
    return serve_frontend(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Always serve static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve frontend files (both in development and production)
frontend_dir = settings.BASE_DIR.parent / 'frontend'
if os.path.exists(frontend_dir):
    urlpatterns += [
        path('', root_view, name='root'),
        path('<path:path>', serve_frontend, name='frontend'),
    ]
else:
    # Fallback if frontend directory doesn't exist
    def fallback_view(request):
        return JsonResponse({
            'message': 'Boss Shop API is running!',
            'status': 'OK',
            'api_endpoints': {
                'health': '/api/health/',
                'admin': '/admin/',
                'api': '/api/'
            },
            'note': 'Frontend files not found'
        })
    
    urlpatterns += [
        path('', fallback_view, name='root'),
    ]