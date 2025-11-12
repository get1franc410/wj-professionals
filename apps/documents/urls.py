# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\documents\urls.py
from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.DocumentListView.as_view(), name='document_list'),
    path('<int:document_id>/', views.document_detail_view, name='document_detail'),
    path('download/<int:document_id>/', views.download_document, name='document_download'),
    path('upload/', views.upload_document_view, name='upload_document'),
    path('category/<slug:category_slug>/', views.category_view, name='category_detail'),
]
