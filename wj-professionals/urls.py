# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\wj_professionals\urls.py
"""
URL configuration for wj_professionals project.

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

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('', include('apps.core.urls')),
    path('staff/', include('apps.staff.urls')),
    path('documents/', include('apps.documents.urls')),
    path('portfolio/', include('apps.portfolio.urls')),
    path('news/', include('apps.news.urls')),
    path('contact/', include('apps.contact.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('software/', include('apps.software.urls')),
    path('reviews/', include('apps.reviews.urls')),

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "WJ Professionals Admin"
admin.site.site_title = "WJ Professionals"
admin.site.index_title = "Welcome to WJ Professionals Administration"
