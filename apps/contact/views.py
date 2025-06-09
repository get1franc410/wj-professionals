# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\contact\views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import ContactSubmission, OfficeLocation
from .forms import ContactForm

def contact_view(request):
    """Contact page with form submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the submission
            submission = form.save(commit=False)
            
            # Add metadata
            submission.ip_address = request.META.get('REMOTE_ADDR')
            submission.user_agent = request.META.get('HTTP_USER_AGENT', '')
            submission.referrer = request.META.get('HTTP_REFERER', '')
            
            submission.save()
            
            # Send notification email to admin
            send_contact_notification(submission)
            
            # Send confirmation email to user
            send_contact_confirmation(submission)
            
            messages.success(
                request, 
                "Thank you for your message! We'll get back to you within 24 hours."
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            
            return redirect('contact:contact')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'office_locations': OfficeLocation.objects.filter(is_active=True),
        'headquarters': OfficeLocation.objects.filter(
            is_headquarters=True, 
            is_active=True
        ).first(),
        'company_emails': settings.COMPANY_EMAILS,
    }
    return render(request, 'contact/contact.html', context)

def send_contact_notification(submission):
    """Send notification email to admin about new contact submission"""
    subject = f"New Contact Form Submission: {submission.subject}"
    
    # Determine recipient based on inquiry type
    recipient_map = {
        'tax': settings.COMPANY_EMAILS.get('tax'),
        'audit': settings.COMPANY_EMAILS.get('audit'),
        'consulting': settings.COMPANY_EMAILS.get('consulting'),
    }
    
    recipient = recipient_map.get(
        submission.inquiry_type, 
        settings.COMPANY_EMAILS.get('admin')
    )
    
    context = {
        'submission': submission,
        'admin_url': f"{settings.SITE_URL}/admin/contact/contactsubmission/{submission.id}/change/"
    }
    
    html_message = render_to_string('contact/emails/admin_notification.html', context)
    plain_message = render_to_string('contact/emails/admin_notification.txt', context)
    
    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient],
        reply_to=[submission.email]
    )
    email.content_subtype = 'html'
    
    # Attach files if any
    for field_name in ['attachment_1', 'attachment_2', 'attachment_3']:
        attachment = getattr(submission, field_name)
        if attachment:
            email.attach_file(attachment.path)
    
    try:
        email.send()
    except Exception as e:
        # Log the error but don't fail the submission
        print(f"Failed to send admin notification: {e}")

def send_contact_confirmation(submission):
    """Send confirmation email to the user"""
    subject = f"Thank you for contacting WJ Professionals - {submission.subject}"
    
    context = {
        'submission': submission,
        'company_name': 'WJ Professionals',
    }
    
    html_message = render_to_string('contact/emails/user_confirmation.html', context)
    plain_message = render_to_string('contact/emails/user_confirmation.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[submission.email],
            fail_silently=False,
        )
    except Exception as e:
        # Log the error but don't fail the submission
        print(f"Failed to send user confirmation: {e}")

def office_locations_view(request):
    """View all office locations"""
    locations = OfficeLocation.objects.filter(is_active=True)
    
    context = {
        'locations': locations,
        'headquarters': locations.filter(is_headquarters=True).first(),
    }
    return render(request, 'contact/office_locations.html', context)

def get_office_info(request, office_id):
    """AJAX endpoint to get office information"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            office = OfficeLocation.objects.get(id=office_id, is_active=True)
            data = {
                'name': office.name,
                'address': office.address,
                'city': office.city,
                'state': office.state,
                'phone': office.phone,
                'email': office.email,
                'office_hours': office.office_hours,
                'latitude': float(office.latitude) if office.latitude else None,
                'longitude': float(office.longitude) if office.longitude else None,
            }
            return JsonResponse({'success': True, 'office': data})
        except OfficeLocation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Office not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
