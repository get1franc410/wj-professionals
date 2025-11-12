# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\reviews\admin.py
from django.contrib import admin
from .models import Review, ReviewResponse

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'rating', 'status', 'created_at', 'is_featured']
    list_filter = ['status', 'rating', 'is_featured', 'created_at']
    search_fields = ['client_name', 'client_email', 'title', 'review_text']
    readonly_fields = ['created_at', 'updated_at', 'ip_address']
    actions = ['approve_reviews', 'feature_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} reviews approved.")
    approve_reviews.short_description = "Approve selected reviews"
    
    def feature_reviews(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} reviews featured.")
    feature_reviews.short_description = "Feature selected reviews"

@admin.register(ReviewResponse)
class ReviewResponseAdmin(admin.ModelAdmin):
    list_display = ['review', 'responder_name', 'created_at']
    search_fields = ['review__client_name', 'response_text']
