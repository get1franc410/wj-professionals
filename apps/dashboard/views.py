# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\dashboard\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from apps.news.models import NewsArticle, NewsCategory
from apps.documents.models import Document, DocumentCategory
from apps.portfolio.models import Client
from apps.contact.models import ContactSubmission, ContactResponse
from apps.staff.models import Staff
from .forms import ArticleForm, DocumentUploadForm

def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_or_admin)
def dashboard_home(request):
    """Main dashboard view"""
    # Get date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Basic statistics
    stats = {
        'total_articles': NewsArticle.objects.count(),
        'published_articles': NewsArticle.objects.filter(status='published').count(),
        'total_documents': Document.objects.count(),
        'total_clients': Client.objects.count(),
        'total_contacts': ContactSubmission.objects.count(),
        'new_contacts_week': ContactSubmission.objects.filter(
            created_at__date__gte=week_ago
        ).count(),
        'pending_contacts': ContactSubmission.objects.filter(
            status='new'
        ).count(),
    }
    
    # Recent activity
    # Recent activity
    recent_contacts = ContactSubmission.objects.order_by('-created_at')[:5]
    recent_articles = NewsArticle.objects.order_by('-created_at')[:5]
    recent_documents = Document.objects.order_by('-created_at')[:5]
    
    # Chart data for the last 30 days
    chart_data = []
    for i in range(30):
        date = today - timedelta(days=i)
        chart_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'contacts': ContactSubmission.objects.filter(
                created_at__date=date
            ).count(),
            'articles': NewsArticle.objects.filter(
                created_at__date=date
            ).count(),
        })
    
    context = {
        'stats': stats,
        'total_messages': ContactSubmission.objects.count(),
        'unread_messages': ContactSubmission.objects.filter(status='new').count(),
        'recent_contacts': recent_contacts,
        'recent_articles': recent_articles,
        'recent_documents': recent_documents,
        'chart_data': list(reversed(chart_data)),
    }
    return render(request, 'dashboard/home.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def email_dashboard(request):
    """Email management dashboard"""
    contacts = ContactSubmission.objects.all().order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status', 'all')
    if status == 'unread':
        contacts = contacts.filter(status='new')
    elif status == 'read':
        contacts = contacts.exclude(status='new')
    
    # Pagination
    paginator = Paginator(contacts, 20)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    
    context = {
        'messages': contacts,  # Use 'messages' for template compatibility
        'unread_count': ContactSubmission.objects.filter(status='new').count(),
        'total_count': ContactSubmission.objects.count(),
        'current_status': status,
    }
    return render(request, 'dashboard/email_dashboard.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def email_detail(request, message_id):
    """Get email details for AJAX"""
    try:
        contact = ContactSubmission.objects.get(id=message_id)
        data = {
            'name': contact.full_name,  # Use the property from model
            'email': contact.email,
            'phone': contact.phone,
            'subject': contact.subject,
            'message': contact.message,
            'created_at': contact.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'company': contact.company,
            'inquiry_type': contact.get_inquiry_type_display(),
            'priority': contact.get_priority_display(),
        }
        return JsonResponse(data)
    except ContactSubmission.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)

@login_required
@user_passes_test(is_staff_or_admin)
def mark_email_read(request, message_id):
    """Mark email as read"""
    if request.method == 'POST':
        contact = get_object_or_404(ContactSubmission, id=message_id)
        contact.status = 'in_progress'  # Change from 'new' to 'in_progress'
        contact.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
@user_passes_test(is_staff_or_admin)
def reply_email(request, message_id):
    """Reply to email"""
    contact = get_object_or_404(ContactSubmission, id=message_id)
    
    if request.method == 'POST':
        reply_content = request.POST.get('reply_content')
        email_subject = request.POST.get('email_subject', f"Re: {contact.subject}")
        
        # Send reply email
        from django.core.mail import send_mail
        from django.conf import settings
        
        email_content = f"""
        Dear {contact.full_name},
        
        {reply_content}
        
        Best regards,
        Wole Joshua & Co. Team
        
        ---
        Original Message:
        From: {contact.full_name} <{contact.email}>
        Subject: {contact.subject}
        Date: {contact.created_at}
        
        {contact.message}
        """
        
        try:
            send_mail(
                email_subject,
                email_content,
                settings.DEFAULT_FROM_EMAIL,
                [contact.email],
                fail_silently=False,
            )
            
            # Create response record
            ContactResponse.objects.create(
                submission=contact,
                responder=request.user,
                response_text=reply_content,
                email_sent=True,
                email_subject=email_subject,
            )
            
            # Update contact status
            contact.response_sent = True
            contact.response_date = timezone.now()
            contact.status = 'resolved'
            contact.save()
            
            messages.success(request, 'Reply sent successfully!')
            return redirect('dashboard:email_dashboard')
            
        except Exception as e:
            messages.error(request, f'Failed to send reply: {str(e)}')
    
    context = {
        'contact': contact,
        'suggested_subject': f"Re: {contact.subject}",
    }
    return render(request, 'dashboard/reply_email.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def manage_articles(request):
    """Manage news articles"""
    articles = NewsArticle.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        articles = articles.filter(status=status_filter)
    
    # Search
    search = request.GET.get('search')
    if search:
        articles = articles.filter(
            Q(title__icontains=search) | 
            Q(excerpt__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(articles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': NewsArticle.STATUS_CHOICES,
        'selected_status': status_filter,
        'search_query': search,
    }
    return render(request, 'dashboard/articles/list.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def create_article(request):
    """Create new article"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            if article.status == 'published' and not article.publish_date:
                from django.utils import timezone
                article.publish_date = timezone.now()

            article.save()
            messages.success(request, 'Article created successfully!')
            return redirect('dashboard:manage_articles')
        else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = ArticleForm()
        
        context = {
            'form': form,
            'categories': NewsCategory.objects.filter(is_active=True),
        }
        return render(request, 'dashboard/articles/create.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def edit_article(request, article_id):
    """Edit existing article"""
    article = get_object_or_404(NewsArticle, id=article_id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            
            # Handle action buttons
            action = request.POST.get('action')
            if action == 'publish':
                article.status = 'published'
                if not article.publish_date:
                    from django.utils import timezone
                    article.publish_date = timezone.now()
            elif action == 'save_draft':
                article.status = 'draft'
            
            article.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('dashboard:manage_articles')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ArticleForm(instance=article)
    
    context = {
        'form': form,
        'article': article,
        'categories': NewsCategory.objects.filter(is_active=True),
    }
    return render(request, 'dashboard/articles/edit.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
@require_POST
def delete_article(request, article_id):
    """Delete article via AJAX"""
    try:
        article = get_object_or_404(NewsArticle, id=article_id)
        
        # Check if user has permission to delete this article
        if not (request.user.is_superuser or article.author == request.user):
            return JsonResponse({
                'success': False, 
                'message': 'You do not have permission to delete this article.'
            }, status=403)
        
        # Store article title for success message
        article_title = article.title
        
        # Delete the article
        article.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Article "{article_title}" has been deleted successfully.'
        })
        
    except NewsArticle.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Article not found.'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)

@login_required
@user_passes_test(is_staff_or_admin)
def manage_contacts(request):
    """Manage contact submissions"""
    contacts = ContactSubmission.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        contacts = contacts.filter(status=status_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority')
    if priority_filter:
        contacts = contacts.filter(priority=priority_filter)
    
    # Filter by inquiry type
    inquiry_filter = request.GET.get('inquiry_type')
    if inquiry_filter:
        contacts = contacts.filter(inquiry_type=inquiry_filter)
    
    # Search
    search = request.GET.get('search')
    if search:
        contacts = contacts.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(subject__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(contacts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': ContactSubmission.STATUS_CHOICES,
        'priority_choices': ContactSubmission.PRIORITY_CHOICES,
        'inquiry_choices': ContactSubmission.INQUIRY_TYPES,
        'selected_status': status_filter,
        'selected_priority': priority_filter,
        'selected_inquiry': inquiry_filter,
        'search_query': search,
    }
    return render(request, 'dashboard/contacts/list.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def contact_detail(request, contact_id):
    """View contact submission details"""
    contact = get_object_or_404(ContactSubmission, id=contact_id)
    
    if request.method == 'POST':
        # Update contact status, priority, or assignment
        action = request.POST.get('action')
        
        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in dict(ContactSubmission.STATUS_CHOICES):
                contact.status = new_status
                contact.save()
                messages.success(request, 'Status updated successfully!')
        
        elif action == 'update_priority':
            new_priority = request.POST.get('priority')
            if new_priority in dict(ContactSubmission.PRIORITY_CHOICES):
                contact.priority = new_priority
                contact.save()
                messages.success(request, 'Priority updated successfully!')
        
        elif action == 'assign':
            staff_id = request.POST.get('assigned_to')
            if staff_id:
                try:
                    staff_member = Staff.objects.get(id=staff_id)
                    contact.assigned_to = staff_member.user
                    contact.save()
                    messages.success(request, f'Assigned to {staff_member.full_name}!')
                except Staff.DoesNotExist:
                    messages.error(request, 'Invalid staff member selected.')
        
        return redirect('dashboard:contact_detail', contact_id=contact_id)
    
    context = {
        'contact': contact,
        'staff_members': Staff.objects.filter(is_active=True),
        'responses': contact.responses.all(),
    }
    return render(request, 'dashboard/contacts/detail.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def manage_documents(request):
    """Manage documents"""
    documents = Document.objects.all().order_by('-created_at')
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        documents = documents.filter(category_id=category_filter)
    
    # Filter by access level
    access_filter = request.GET.get('access_level')
    if access_filter:
        documents = documents.filter(access_level=access_filter)
    
    # Search
    search = request.GET.get('search')
    if search:
        documents = documents.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(documents, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': DocumentCategory.objects.filter(is_active=True),
        'access_levels': Document.ACCESS_LEVELS,
        'selected_category': category_filter,
        'selected_access': access_filter,
        'search_query': search,
    }
    return render(request, 'dashboard/documents/list.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def upload_document(request):
    """Upload new document"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('dashboard:manage_documents')
    else:
        form = DocumentUploadForm()
    
    context = {
        'form': form,
        'categories': DocumentCategory.objects.filter(is_active=True),
    }
    return render(request, 'dashboard/documents/upload.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
def analytics_view(request):
    """Analytics dashboard"""
    # Time range
    days = int(request.GET.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Contact analytics
    contact_data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        count = ContactSubmission.objects.filter(created_at__date=date).count()
        contact_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Document download analytics
    from apps.documents.models import DownloadLog
    download_data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        count = DownloadLog.objects.filter(download_date__date=date).count()
        download_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Popular documents
    popular_docs = Document.objects.filter(
        is_active=True
    ).order_by('-download_count')[:10]
    
    # Popular articles
    popular_articles = NewsArticle.objects.filter(
        status='published'
    ).order_by('-view_count')[:10]
    
    context = {
        'contact_data': contact_data,
        'download_data': download_data,
        'popular_docs': popular_docs,
        'popular_articles': popular_articles,
        'days': days,
    }
    return render(request, 'dashboard/analytics.html', context)

# AJAX endpoints
@login_required
@user_passes_test(is_staff_or_admin)
def quick_stats_api(request):
    """API endpoint for dashboard quick stats"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        today = timezone.now().date()
        
        stats = {
            'new_contacts_today': ContactSubmission.objects.filter(
                created_at__date=today
            ).count(),
            'pending_contacts': ContactSubmission.objects.filter(
                status='new'
            ).count(),
            'draft_articles': NewsArticle.objects.filter(
                status='draft'
            ).count(),
            'total_documents': Document.objects.filter(is_active=True).count(),
        }
        
        return JsonResponse(stats)
    
    return JsonResponse({'error': 'Invalid request'})
