# apps/core/admin.py (create if missing)
from django.contrib import admin
from .models import Visitor

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'ip', 'user', 'country', 'city', 'path')
    list_filter = ('country', 'city', 'path', 'created_at')
    search_fields = ('ip', 'user__username', 'path', 'user_agent', 'referer')
