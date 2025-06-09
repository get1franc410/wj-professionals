# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\dashboard\urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),

    path('', views.dashboard_home, name='home'),
    
    path('emails/', views.email_dashboard, name='email_dashboard'),
    path('email/<int:message_id>/', views.email_detail, name='email_detail'),
    path('email/<int:message_id>/mark-read/', views.mark_email_read, name='mark_email_read'),
    path('email/<int:message_id>/reply/', views.reply_email, name='reply_email'),
    # Articles management
    path('articles/', views.manage_articles, name='manage_articles'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('articles/delete/<int:article_id>/', views.delete_article, name='delete_article'),
    
    # Contact management
    path('contacts/', views.manage_contacts, name='manage_contacts'),
    path('contacts/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    
    # Document management
    path('documents/', views.manage_documents, name='manage_documents'),
    path('documents/upload/', views.upload_document, name='upload_document'),
    
    # Analytics
    path('analytics/', views.analytics_view, name='analytics'),
    
    # API endpoints
    path('api/quick-stats/', views.quick_stats_api, name='quick_stats_api'),
]
