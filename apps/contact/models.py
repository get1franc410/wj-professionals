# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\contact\models.py
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class ContactSubmission(models.Model):
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('tax', 'Tax Services'),
        ('audit', 'Audit Services'),
        ('consulting', 'Business Consulting'),
        ('bookkeeping', 'Bookkeeping'),
        ('quote', 'Request Quote'),
        ('complaint', 'Complaint'),
        ('partnership', 'Partnership Opportunity'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=100, blank=True)
    
    # Inquiry Details
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = CKEditor5Field('Message', config_name='default')
    
    # Additional Information
    preferred_contact_method = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('both', 'Both'),
    ], default='email')
    
    budget_range = models.CharField(max_length=50, blank=True, choices=[
        ('under_100k', 'Under ₦100,000'),
        ('100k_500k', '₦100,000 - ₦500,000'),
        ('500k_1m', '₦500,000 - ₦1,000,000'),
        ('1m_5m', '₦1,000,000 - ₦5,000,000'),
        ('over_5m', 'Over ₦5,000,000'),
        ('discuss', 'Prefer to Discuss'),
    ])
    
    timeline = models.CharField(max_length=50, blank=True, choices=[
        ('immediate', 'Immediate'),
        ('1_week', 'Within 1 Week'),
        ('1_month', 'Within 1 Month'),
        ('3_months', 'Within 3 Months'),
        ('flexible', 'Flexible'),
    ])
    
    # File Attachments
    attachment_1 = models.FileField(upload_to='contact_docs/', blank=True)
    attachment_2 = models.FileField(upload_to='contact_docs/', blank=True)
    attachment_3 = models.FileField(upload_to='contact_docs/', blank=True)
    
    # Internal Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Response Tracking
    response_sent = models.BooleanField(default=False)
    response_date = models.DateTimeField(blank=True, null=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(blank=True, null=True)
    
    # Internal Notes
    internal_notes = CKEditor5Field('Internal Notes', config_name='default', blank=True, 
                                   help_text="Internal notes for staff")
    
    # Metadata
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    # GDPR Compliance
    consent_marketing = models.BooleanField(default=False)
    consent_data_processing = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
    
    def send_notification(self):
        """Send notification to admin email"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f'New Contact Message: {self.subject}'
        message = f"""
        New contact message received on Wole Joshua & Co. website:
        
        From: {self.full_name}
        Email: {self.email}
        Phone: {self.phone}
        Company: {self.company}
        Subject: {self.subject}
        Type: {self.get_inquiry_type_display()}
        Priority: {self.get_priority_display()}
        
        Message:
        {self.message}
        
        ---
        Received: {self.created_at}
        View in dashboard: {settings.SITE_URL}/dashboard/emails/
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send notification email: {e}")

    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class ContactResponse(models.Model):
    submission = models.ForeignKey(ContactSubmission, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    response_text = CKEditor5Field('Response', config_name='default')
    
    # Email Details
    email_sent = models.BooleanField(default=False)
    email_subject = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Response to {self.submission.full_name}"

class OfficeLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default="Nigeria")
    
    # Contact Details
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    fax = models.CharField(max_length=20, blank=True)
    
    # Map Coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Office Details
    office_hours = models.TextField(help_text="e.g., Mon-Fri: 8:00 AM - 6:00 PM")
    services_available = models.JSONField(default=list)
    
    # Settings
    is_headquarters = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.city}"

