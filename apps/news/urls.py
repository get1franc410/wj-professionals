# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\news\urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='article_list'),
    path('article/<slug:slug>/', views.NewsDetailView.as_view(), name='article_detail'),
    path('category/<slug:slug>/', views.category_view, name='category_detail'),
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('like/<int:article_id>/', views.like_article, name='like_article'),
]
