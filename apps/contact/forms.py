# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\contact\forms.py
"""
Contact Forms
=============
Forms for contact submissions, responses, and management
"""

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django_ckeditor_5.widgets import CKEditor5Widget
import os

from .models import ContactSubmission, ContactResponse, OfficeLocation


class ContactForm(forms.ModelForm):
    """Main contact form for website visitors"""
    
    # Additional fields not in model
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
            'required': True
        })
    )
    
    newsletter_subscribe = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Subscribe to our newsletter"
    )
    
    # Honeypot field for spam protection
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = ContactSubmission
        fields = [
            'email', 'phone', 'company', 'position', 'inquiry_type',
            'subject', 'message', 'preferred_contact_method', 'budget_range',
            'timeline', 'attachment_1', 'attachment_2', 'attachment_3',
            'consent_marketing', 'consent_data_processing'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+234 xxx xxx xxxx',
                'pattern': r'^\+?[\d\s\-\(\)]+$'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your company or organization'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your job title or position'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of your inquiry',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Please provide details about your inquiry...',
                'required': True
            }),
            'preferred_contact_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'budget_range': forms.Select(attrs={
                'class': 'form-select'
            }),
            'timeline': forms.Select(attrs={
                'class': 'form-select'
            }),
            'attachment_1': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png'
            }),
            'attachment_2': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png'
            }),
            'attachment_3': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png'
            }),
            'consent_marketing': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'consent_data_processing': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set field labels and help texts
        self.fields['email'].help_text = "We'll use this to respond to your inquiry"
        self.fields['phone'].help_text = "Include country code for international numbers"
        self.fields['inquiry_type'].help_text = "Select the service you're most interested in"
        self.fields['budget_range'].help_text = "This helps us provide appropriate recommendations"
        self.fields['timeline'].help_text = "When do you need this service?"
        self.fields['attachment_1'].help_text = "Upload relevant documents (Max 10MB each)"
        self.fields['consent_data_processing'].help_text = "Required to process your inquiry"
        self.fields['consent_marketing'].help_text = "Optional: Receive updates about our services"
        
        # Set required fields
        self.fields['consent_data_processing'].required = True
        
        # Set initial values
        self.fields['preferred_contact_method'].initial = 'email'
        self.fields['consent_data_processing'].initial = True

    def clean_website(self):
        """Honeypot field validation"""
        website = self.cleaned_data.get('website')
        if website:
            raise ValidationError("Spam detected.")
        return website

    def clean_name(self):
        """Split name into first and last name"""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Name is required.")
        
        # Split name into first and last
        name_parts = name.split()
        if len(name_parts) < 2:
            raise ValidationError("Please provide both first and last name.")
        
        return name

    def clean_email(self):
        """Validate email format and domain"""
        email = self.cleaned_data.get('email', '').lower()
        
        # Check for common disposable email domains
        disposable_domains = [
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'throwaway.email'
        ]
        
        domain = email.split('@')[-1] if '@' in email else ''
        if domain in disposable_domains:
            raise ValidationError("Please use a permanent email address.")
        
        return email

    def clean_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('phone', '').strip()
        if phone:
            # Remove common separators
            cleaned_phone = ''.join(char for char in phone if char.isdigit() or char == '+')
            
            # Basic validation
            if len(cleaned_phone) < 10:
                raise ValidationError("Please enter a valid phone number.")
            
            return phone
        return phone

    def clean_subject(self):
        """Validate subject line"""
        subject = self.cleaned_data.get('subject', '').strip()
        
        # Check for spam keywords
        spam_keywords = ['free', 'urgent', 'act now', 'limited time']
        if any(keyword in subject.lower() for keyword in spam_keywords):
            # Don't block completely, just flag for review
            pass
        
        return subject

    def clean_message(self):
        """Validate message content"""
        message = self.cleaned_data.get('message', '').strip()
        
        if len(message) < 20:
            raise ValidationError("Please provide more details in your message (minimum 20 characters).")
        
        if len(message) > 5000:
            raise ValidationError("Message is too long (maximum 5000 characters).")
        
        return message

    def clean_attachment_1(self):
        return self._clean_attachment('attachment_1')

    def clean_attachment_2(self):
        return self._clean_attachment('attachment_2')

    def clean_attachment_3(self):
        return self._clean_attachment('attachment_3')

    def _clean_attachment(self, field_name):
        """Common attachment validation"""
        attachment = self.cleaned_data.get(field_name)
        if attachment:
            # Check file size (max 10MB)
            max_size = 10 * 1024 * 1024
            if attachment.size > max_size:
                raise ValidationError(f"File size cannot exceed 10MB. Current size: {attachment.size / (1024*1024):.1f}MB")
            
            # Check file extension
            allowed_extensions = [
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', 
                '.jpg', '.jpeg', '.png', '.gif', '.txt'
            ]
            file_extension = os.path.splitext(attachment.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    f"File type '{file_extension}' not supported. "
                    f"Allowed types: {', '.join(allowed_extensions)}"
                )
        
        return attachment

    def save(self, commit=True):
        """Custom save method to handle name splitting"""
        instance = super().save(commit=False)
        
        # Split name into first and last
        name = self.cleaned_data.get('name', '')
        name_parts = name.split()
        instance.first_name = name_parts[0]
        instance.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        if commit:
            instance.save()
        
        return instance


class QuickContactForm(forms.Form):
    """Simplified contact form for quick inquiries"""
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name',
            'required': True
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': True
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone number'
        })
    )
    
    service = forms.ChoiceField(
        choices=ContactSubmission.INQUIRY_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'How can we help you?',
            'required': True
        })
    )


class ContactResponseForm(forms.ModelForm):
    """Form for staff to respond to contact submissions"""
    
    class Meta:
        model = ContactResponse
        fields = ['response_text', 'email_subject']
        widgets = {
            'response_text': CKEditor5Widget(
                attrs={'class': 'form-control'},
                config_name='default'
            ),
            'email_subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email subject line'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.submission = kwargs.pop('submission', None)
        super().__init__(*args, **kwargs)
        
        if self.submission:
            # Pre-populate subject line
            self.fields['email_subject'].initial = f"Re: {self.submission.subject}"


class ContactFilterForm(forms.Form):
    """Form for filtering contact submissions in admin"""
    
    STATUS_CHOICES = [('', 'All Statuses')] + list(ContactSubmission.STATUS_CHOICES)
    PRIORITY_CHOICES = [('', 'All Priorities')] + list(ContactSubmission.PRIORITY_CHOICES)
    INQUIRY_CHOICES = [('', 'All Types')] + list(ContactSubmission.INQUIRY_TYPES)
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search contacts...'
        })
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    inquiry_type = forms.ChoiceField(
        choices=INQUIRY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True, is_active=True),
        required=False,
        empty_label="All Staff",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


class OfficeLocationForm(forms.ModelForm):
    """Form for managing office locations"""
    
    class Meta:
        model = OfficeLocation
        fields = [
            'name', 'address', 'city', 'state', 'postal_code', 'country',
            'phone', 'email', 'fax', 'latitude', 'longitude', 'office_hours',
            'services_available', 'is_headquarters', 'is_active', 'order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Office name'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal/ZIP code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+234 xxx xxx xxxx'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'office@example.com'
            }),
            'fax': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fax number (optional)'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Latitude (decimal degrees)'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Longitude (decimal degrees)'
            }),
            'office_hours': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'e.g., Mon-Fri: 8:00 AM - 6:00 PM\nSat: 9:00 AM - 2:00 PM\nSun: Closed'
            }),
            'is_headquarters': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].initial = 'Nigeria'
        self.fields['is_active'].initial = True
        self.fields['order'].initial = 0

    def clean(self):
        cleaned_data = super().clean()
        
        # Only one headquarters allowed
        is_headquarters = cleaned_data.get('is_headquarters')
        if is_headquarters:
            existing_hq = OfficeLocation.objects.filter(is_headquarters=True)
            if self.instance.pk:
                existing_hq = existing_hq.exclude(pk=self.instance.pk)
            
            if existing_hq.exists():
                raise ValidationError("Only one office can be designated as headquarters.")
        
        return cleaned_data


class NewsletterSubscriptionForm(forms.Form):
    """Newsletter subscription form"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'required': True
        })
    )
    
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name (optional)'
        })
    )
    
    interests = forms.MultipleChoiceField(
        choices=[
            ('tax_updates', 'Tax Updates'),
            ('business_tips', 'Business Tips'),
            ('regulatory_changes', 'Regulatory Changes'),
            ('industry_news', 'Industry News'),
            ('company_updates', 'Company Updates'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="I agree to receive newsletters and marketing communications"
    )


class AppointmentRequestForm(forms.Form):
    """Form for requesting appointments"""
    
    APPOINTMENT_TYPES = [
        ('consultation', 'Initial Consultation'),
        ('tax_planning', 'Tax Planning Session'),
        ('business_review', 'Business Review'),
        ('financial_planning', 'Financial Planning'),
        ('audit_discussion', 'Audit Discussion'),
        ('other', 'Other'),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
            'required': True
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': True
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone number',
            'required': True
        })
    )
    
    company = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Company name (if applicable)'
        })
    )
    
    appointment_type = forms.ChoiceField(
        choices=APPOINTMENT_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': '',  # Will be set via JavaScript to today's date
            'required': True
        })
    )
    
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'required': True
        })
    )
    
    alternative_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    alternative_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        })
    )
    
    meeting_preference = forms.ChoiceField(
        choices=[
            ('in_person', 'In-Person Meeting'),
            ('video_call', 'Video Call'),
            ('phone_call', 'Phone Call'),
        ],
        initial='in_person',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Please describe what you would like to discuss...',
            'required': True
        })
    )

    def clean_preferred_date(self):
        """Ensure appointment date is not in the past"""
        from django.utils import timezone
        preferred_date = self.cleaned_data.get('preferred_date')
        
        if preferred_date and preferred_date < timezone.now().date():
            raise ValidationError("Appointment date cannot be in the past.")
        
        return preferred_date

    def clean(self):
        """Validate time combinations"""
        cleaned_data = super().clean()
        
        # If alternative date is provided, alternative time should also be provided
        alt_date = cleaned_data.get('alternative_date')
        alt_time = cleaned_data.get('alternative_time')
        
        if alt_date and not alt_time:
            raise ValidationError("Please provide alternative time if you specify alternative date.")
        
        if alt_time and not alt_date:
            raise ValidationError("Please provide alternative date if you specify alternative time.")
        
        return cleaned_data
