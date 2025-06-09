# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\dashboard\models.py
"""
Dashboard Models
================
This file contains models specific to dashboard functionality.
Most dashboard views use models from other apps (news, documents, contact, etc.)
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.contact.models import ContactSubmission


class DashboardPreference(models.Model):
    """User preferences for dashboard customization"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_preferences')
    default_page_size = models.IntegerField(default=20, choices=[
        (10, '10 items'),
        (20, '20 items'),
        (50, '50 items'),
        (100, '100 items'),
    ])
    default_date_range = models.IntegerField(default=30, choices=[
        (7, 'Last 7 days'),
        (30, 'Last 30 days'),
        (90, 'Last 90 days'),
        (365, 'Last year'),
    ])
    dashboard_widgets = models.JSONField(default=dict, help_text="Widget configuration")
    email_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dashboard Preference"
        verbose_name_plural = "Dashboard Preferences"

    def __str__(self):
        return f"Dashboard preferences for {self.user.username}"


class ActivityLog(models.Model):
    """Log of admin/staff activities"""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('download', 'Download'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    content_type = models.CharField(max_length=100, blank=True)  # e.g., 'article', 'document', 'contact'
    object_id = models.CharField(max_length=100, blank=True)
    object_name = models.CharField(max_length=200, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    additional_data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
            models.Index(fields=['content_type', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"


class SystemAlert(models.Model):
    """System alerts and notifications for dashboard"""
    ALERT_TYPES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES, default='info')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    is_active = models.BooleanField(default=True)
    is_dismissible = models.BooleanField(default=True)
    target_users = models.ManyToManyField(User, blank=True, help_text="Leave empty for all staff users")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_alerts')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "System Alert"
        verbose_name_plural = "System Alerts"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class AlertDismissal(models.Model):
    """Track which alerts users have dismissed"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert = models.ForeignKey(SystemAlert, on_delete=models.CASCADE)
    dismissed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'alert']
        verbose_name = "Alert Dismissal"
        verbose_name_plural = "Alert Dismissals"

    def __str__(self):
        return f"{self.user.username} dismissed {self.alert.title}"


class DashboardWidget(models.Model):
    """Custom dashboard widgets"""
    WIDGET_TYPES = [
        ('stats', 'Statistics'),
        ('chart', 'Chart'),
        ('list', 'List'),
        ('calendar', 'Calendar'),
        ('custom', 'Custom'),
    ]

    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    configuration = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    required_permission = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dashboard Widget"
        verbose_name_plural = "Dashboard Widgets"
        ordering = ['order', 'name']

    def __str__(self):
        return self.title


class QuickAction(models.Model):
    """Quick action buttons for dashboard"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default='fas fa-link')
    color = models.CharField(max_length=20, default='primary')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    required_permission = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quick Action"
        verbose_name_plural = "Quick Actions"
        ordering = ['order', 'name']

    def __str__(self):
        return self.title
