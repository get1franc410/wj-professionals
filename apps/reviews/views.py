# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\reviews\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q  # ✅ Added Q import
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Review
from .forms import ReviewForm

def add_review(request):
    """Add a new review"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                review.ip_address = x_forwarded_for.split(',')[0]
            else:
                review.ip_address = request.META.get('REMOTE_ADDR')
            
            review.save()
            
            messages.success(
                request, 
                'Thank you for your review! It will be published after moderation.'
            )
            return redirect('reviews:review_success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'page_title': 'Leave a Review',
    }
    return render(request, 'reviews/add_review.html', context)

def review_success(request):
    """Thank you page after review submission"""
    return render(request, 'reviews/review_success.html')

def review_list(request):
    """Display all approved reviews"""
    reviews = Review.objects.filter(status='approved').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(reviews, 12)  # 12 reviews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    stats = Review.objects.filter(status='approved').aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    
    context = {
        'page_obj': page_obj,
        'reviews': page_obj,
        'stats': stats,
        'page_title': 'Client Reviews',
    }
    return render(request, 'reviews/review_list.html', context)

@require_http_methods(["GET"])
def review_stats_api(request):
    """API endpoint for review statistics"""
    stats = Review.objects.filter(status='approved').aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id'),
        five_star=Count('id', filter=Q(rating=5)),  # ✅ Fixed: using Q() instead of models.Q()
        four_star=Count('id', filter=Q(rating=4)),
        three_star=Count('id', filter=Q(rating=3)),
        two_star=Count('id', filter=Q(rating=2)),
        one_star=Count('id', filter=Q(rating=1)),
    )
    
    return JsonResponse(stats)
