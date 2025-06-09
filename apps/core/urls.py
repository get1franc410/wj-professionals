# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\core\urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('tax-calculators/', views.tax_calculator_view, name='tax_calculators'),
    path('faq/', views.faq_view, name='faq'),
    path('search/', views.search_view, name='search'),
    path('admin-access/', views.admin_access, name='admin_access'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]
