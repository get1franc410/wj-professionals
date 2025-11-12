# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\dashboard\context_processors.py
from apps.contact.models import ContactSubmission

def dashboard_context(request):
    """Add dashboard-specific context variables"""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return {
            'unread_messages_count': ContactSubmission.objects.filter(status='new').count(),
            'pending_reviews_count': 0,  # Add when review model is available
        }
    return {}
