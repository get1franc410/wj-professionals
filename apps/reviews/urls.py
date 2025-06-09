# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\reviews\urls.py
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/', views.add_review, name='add_review'),
    path('success/', views.review_success, name='review_success'),
    path('all/', views.review_list, name='review_list'),
    path('api/stats/', views.review_stats_api, name='review_stats_api'),
]
