# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\documents\models.py
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field 
from django.utils.text import slugify
import os

class DocumentCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = CKEditor5Field('Description', config_name='default')
    icon = models.CharField(max_length=50, default="fas fa-folder")
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Document Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Document(models.Model):
    ACCESS_LEVELS = [
        ('public', 'Public'),
        ('registered', 'Registered Users Only'),
        ('staff', 'Staff Only'),
        ('admin', 'Admin Only'),
    ]
    
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Description', config_name='default')
    file = models.FileField(upload_to='documents/')
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)
    
    # Access Control
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS, default='public')
    requires_approval = models.BooleanField(default=False)
    
    # File Information
    file_size = models.PositiveIntegerField(blank=True, null=True)
    file_type = models.CharField(max_length=50, blank=True)
    
    # Metadata
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Analytics
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    
    # SEO
    meta_description = models.TextField(max_length=160, blank=True)
    tags = models.JSONField(default=list, help_text="List of tags for searching")
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.file_type = os.path.splitext(self.file.name)[1].lower()
        super().save(*args, **kwargs)
    
    @property
    def file_size_mb(self):
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0

class DownloadLog(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='download_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    download_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-download_date']
    
    def __str__(self):
        return f"{self.document.title} - {self.download_date}"
