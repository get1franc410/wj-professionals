# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\staff\urls.py
from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team'),
    path('<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
    path('department/<int:department_id>/', views.department_view, name='department_detail'),
]
