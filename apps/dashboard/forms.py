# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\dashboard\forms.py
"""
Dashboard Forms
===============
Forms for dashboard functionality including article creation, document upload, etc.
"""

from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.news.models import NewsArticle, NewsCategory
from apps.documents.models import Document, DocumentCategory
from apps.contact.models import ContactSubmission, ContactResponse
from .models import DashboardPreference, SystemAlert


class ArticleForm(forms.ModelForm):
    """Form for creating/editing news articles"""

    content = forms.CharField(widget=CKEditor5Widget(config_name='extends'))
    
    class Meta:
        model = NewsArticle
        fields = [
            'title', 'slug', 'excerpt', 'content', 'category', 
            'featured_image', 'status', 'is_featured', 'is_breaking',
            'meta_description', 'tags', 'allow_comments'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title...'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'url-friendly-slug'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief summary of the article...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Article content...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'SEO meta description...',
                'maxlength': 160
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'tag1, tag2, tag3...'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_breaking': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'allow_comments': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = NewsCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Select Category"
        
        # Make slug optional for new articles (auto-generate from title)
        if not self.instance.pk:
            self.fields['slug'].required = False

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title')
        
        # Auto-generate slug if not provided
        if not slug and title:
            from django.utils.text import slugify
            slug = slugify(title)
        
        # Check for uniqueness
        if slug:
            qs = NewsArticle.objects.filter(slug=slug)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("This slug is already in use.")
        
        return slug


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading documents"""
    
    class Meta:
        model = Document
        fields = [
            'title', 'description', 'category', 'file', 'access_level',
            'is_featured', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Document description'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx'
            }),
            'access_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = DocumentCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Select a category"

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 50MB)
            if file.size > 50 * 1024 * 1024:
                raise ValidationError("File size cannot exceed 50MB.")
        return file

class ContactFilterForm(forms.Form):
    """Form for filtering contact submissions"""
    
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



class DashboardPreferenceForm(forms.ModelForm):
    """Form for dashboard preferences"""
    
    class Meta:
        model = DashboardPreference
        fields = [
            'default_page_size', 'default_date_range',
            'email_notifications'
        ]
        widgets = {
            'default_page_size': forms.Select(attrs={
                'class': 'form-select'
            }),
            'default_date_range': forms.Select(attrs={
                'class': 'form-select'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class SystemAlertForm(forms.ModelForm):
    """Form for creating system alerts"""
    
    class Meta:
        model = SystemAlert
        fields = [
            'title', 'message', 'alert_type', 'priority',
            'is_dismissible', 'target_users', 'expires_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Alert title'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Alert message'
            }),
            'alert_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_dismissible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'target_users': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target_users'].queryset = User.objects.filter(
            is_staff=True, is_active=True
        ).order_by('first_name', 'last_name', 'username')
        self.fields['target_users'].help_text = "Leave empty to show to all staff users"


class BulkActionForm(forms.Form):
    """Form for bulk actions on various objects"""
    
    ACTION_CHOICES = [
        ('', 'Select action...'),
        ('delete', 'Delete selected'),
        ('activate', 'Activate selected'),
        ('deactivate', 'Deactivate selected'),
        ('export', 'Export selected'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    selected_items = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    def clean_selected_items(self):
        items = self.cleaned_data.get('selected_items', '')
        if not items:
            raise ValidationError("No items selected.")
        
        try:
            item_ids = [int(x) for x in items.split(',') if x.strip()]
            if not item_ids:
                raise ValidationError("No valid items selected.")
            return item_ids
        except ValueError:
            raise ValidationError("Invalid item selection.")


class QuickSearchForm(forms.Form):
    """Quick search form for dashboard"""
    
    SEARCH_TYPES = [
        ('all', 'All'),
        ('articles', 'Articles'),
        ('documents', 'Documents'),
        ('contacts', 'Contacts'),
    ]
    
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quick search...',
            'autocomplete': 'off'
        })
    )
    search_type = forms.ChoiceField(
        choices=SEARCH_TYPES,
        initial='all',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
