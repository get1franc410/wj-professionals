from django.http import HttpResponse
from django.shortcuts import render
import traceback

def debug_home(request):
    try:
        # Test all imports
        from apps.core.models import Company
        company = Company.objects.first()
        
        from apps.reviews.models import Review
        reviews = Review.objects.filter(status='approved')
        
        from apps.staff.models import Staff
        staff = Staff.objects.filter(is_active=True)
        
        from apps.news.models import NewsArticle
        news = NewsArticle.objects.filter(status='published')[:3]
        
        return HttpResponse(f'''
        <h1> Debug Success!</h1>
        <p><strong>Company:</strong> {company.name if company else "No company found"}</p>
        <p><strong>Reviews:</strong> {reviews.count()} found</p>
        <p><strong>Staff:</strong> {staff.count()} found</p>
        <p><strong>News:</strong> {news.count()} found</p>
        <p><a href="/admin/">Go to Admin</a></p>
        ''')
        
    except Exception as e:
        error_details = traceback.format_exc()
        return HttpResponse(f'''
        <h1> Debug Error</h1>
        <p><strong>Error:</strong> {str(e)}</p>
        <pre>{error_details}</pre>
        ''')

def simple_home(request):
    return HttpResponse('<h1> Simple View Working!</h1><p>Basic Django is working fine.</p>')
