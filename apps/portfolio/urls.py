# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\portfolio\urls.py
from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.ClientPortfolioView.as_view(), name='client_list'),
    path('client/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('industry/<int:industry_id>/', views.industry_view, name='industry_detail'),
    path('case-studies/', views.case_studies_view, name='case_studies'),
    path('case-study/<int:client_id>/', views.case_study_detail_view, name='case_study_detail'),
]
