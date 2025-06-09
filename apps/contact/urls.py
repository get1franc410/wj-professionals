# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\contact\urls.py
from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('offices/', views.office_locations_view, name='office_locations'),
    path('office-info/<int:office_id>/', views.get_office_info, name='office_info'),
]
