# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from apps.core.models import Visitor
import requests

class VisitorLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip admin and static
        if request.path.startswith('/admin') or request.path.startswith(settings.STATIC_URL) or request.path.startswith(settings.MEDIA_URL):
            return

        ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR')
        ua = request.META.get('HTTP_USER_AGENT', '')
        ref = request.META.get('HTTP_REFERER', '')

        country = ''
        city = ''

        # Optional IP geo lookup (toggle via settings)
        if getattr(settings, 'VISITOR_LOOKUP_ENABLED', False) and ip:
            try:
                # Simple free endpoint example; consider caching and rate limits
                r = requests.get(f'https://ipapi.co/{ip}/json/', timeout=1.0)
                if r.ok:
                    data = r.json()
                    country = data.get('country_name') or ''
                    city = data.get('city') or ''
            except Exception:
                pass

        Visitor.objects.create(
            ip=ip or None,
            user=request.user if request.user.is_authenticated else None,
            path=request.path,
            user_agent=ua[:1000],
            referer=ref[:1000],
            country=country[:100] if country else '',
            city=city[:100] if city else '',
        )
