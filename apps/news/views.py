# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\news\views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q, F
from django.urls import reverse
import secrets
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import NewsArticle, NewsCategory, NewsletterSubscriber
from apps.news.forms import NewsletterSubscriptionForm

def send_newsletter_confirmation(subscriber):
    # generate token if missing
    if not subscriber.confirmation_token:
        subscriber.confirmation_token = secrets.token_urlsafe(24)
        subscriber.save(update_fields=['confirmation_token'])
    confirm_url = f"{settings.SITE_URL}{reverse('news:newsletter_confirm', args=[subscriber.confirmation_token])}"
    unsubscribe_url = f"{settings.SITE_URL}{reverse('news:newsletter_unsubscribe', args=[subscriber.confirmation_token])}"

    context = {
        'confirm_url': confirm_url,
        'unsubscribe_url': unsubscribe_url,
        'subscriber': subscriber,
        'company': 'Wole Joshua & Co.',
    }
    subject = "Confirm your subscription - Wole Joshua & Co."
    plain = render_to_string('news/emails/newsletter_confirm.txt', context)
    html = render_to_string('news/emails/newsletter_confirm.html', context)
    send_mail(subject, plain, settings.EMAIL_HOST_USER, [subscriber.email], html_message=html, fail_silently=False)

def newsletter_subscribe(request):
    """Newsletter subscription"""
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            first_name = form.cleaned_data.get('first_name', '')
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name}
            )
            # Always (re)send confirmation if not confirmed
            if not subscriber.confirmed:
                # assign token and send confirmation
                send_newsletter_confirmation(subscriber)
                messages.success(request, "Check your email to confirm your subscription.")
            else:
                messages.info(request, "You are already subscribed.")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'created': created})
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    return redirect('news:article_list')


from django.urls import reverse

def newsletter_confirm(request, token):
    try:
        s = NewsletterSubscriber.objects.get(confirmation_token=token, is_active=True)
        s.confirmed = True
        s.save(update_fields=['confirmed'])
        messages.success(request, "Subscription confirmed. You will receive updates from us.")
    except NewsletterSubscriber.DoesNotExist:
        messages.error(request, "Invalid or expired confirmation link.")
    return redirect('news:article_list')


def newsletter_unsubscribe(request, token):
    try:
        s = NewsletterSubscriber.objects.get(confirmation_token=token, is_active=True)
        s.unsubscribe()  # uses model method already present
        messages.success(request, "You have been unsubscribed.")
    except NewsletterSubscriber.DoesNotExist:
        messages.error(request, "Invalid unsubscribe link.")
    return redirect('news:article_list')

class NewsListView(ListView):
    model = NewsArticle
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = NewsArticle.objects.filter(
            status='published',
            publish_date__lte=timezone.now()
        )
        
        category = self.request.GET.get('category')
        article_type = self.request.GET.get('type')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        
        if article_type:
            queryset = queryset.filter(article_type=article_type)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(excerpt__icontains=search) |
                Q(content__icontains=search) |
                Q(tags__icontains=search)
            )
        
        return queryset.order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.filter(is_active=True)
        context['article_types'] = NewsArticle.ARTICLE_TYPES
        context['featured_articles'] = NewsArticle.objects.filter(
            is_featured=True,
            status='published',
            publish_date__lte=timezone.now()
        )[:3]
        context['breaking_news'] = NewsArticle.objects.filter(
            is_breaking=True,
            status='published',
            publish_date__lte=timezone.now()
        )[:2]
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return NewsArticle.objects.filter(
            status='published',
            publish_date__lte=timezone.now()
        )
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        NewsArticle.objects.filter(id=obj.id).update(view_count=F('view_count') + 1)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_articles'] = NewsArticle.objects.filter(
            category=self.object.category,
            status='published',
            publish_date__lte=timezone.now()
        ).exclude(id=self.object.id)[:3]
        
        context['recent_articles'] = NewsArticle.objects.filter(
            status='published',
            publish_date__lte=timezone.now()
        ).exclude(id=self.object.id)[:5]
        
        context['comments'] = self.object.comments.filter(is_approved=True)
        return context

def category_view(request, slug):
    """View articles by category"""
    category = get_object_or_404(NewsCategory, slug=slug, is_active=True)
    articles = NewsArticle.objects.filter(
        category=category,
        status='published',
        publish_date__lte=timezone.now()
    )
    
    context = {
        'category': category,
        'articles': articles,
        'article_count': articles.count(),
    }
    return render(request, 'news/category_detail.html', context)

def newsletter_subscribe(request):
    """Newsletter subscription"""
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data.get('first_name', '')
            
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name}
            )
            
            if created:
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.info(request, "You're already subscribed to our newsletter.")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'created': created})
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    
    return redirect('news:article_list')

def like_article(request, article_id):
    """AJAX endpoint to like an article"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        article = get_object_or_404(NewsArticle, id=article_id, status='published')
        NewsArticle.objects.filter(id=article_id).update(like_count=F('like_count') + 1)
        
        return JsonResponse({
            'success': True,
            'new_count': article.like_count + 1
        })
    
    return JsonResponse({'success': False})
