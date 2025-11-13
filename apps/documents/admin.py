# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\documents\admin.py
from django.contrib import admin
from .models import DocumentCategory, Document, DownloadLog

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'file_type', 'access_level', 'is_active', 'created_at']
    list_filter = ['category', 'access_level', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['uploaded_by']
    readonly_fields = ['file_size', 'file_type', 'download_count', 'view_count']
