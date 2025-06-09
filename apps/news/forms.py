# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\news\forms.py
"""
News Forms - Simplified
=======================
Essential forms for news functionality
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import NewsArticle, NewsCategory, NewsletterSubscriber, Comment


class NewsletterSubscriptionForm(forms.ModelForm):
    """Simple newsletter subscription form"""
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'first_name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        
        # Check for disposable email domains
        disposable_domains = ['10minutemail.com', 'tempmail.org', 'guerrillamail.com']
        domain = email.split('@')[-1] if '@' in email else ''
        
        if domain in disposable_domains:
            raise ValidationError("Please use a permanent email address.")
        
        return email


class CommentForm(forms.ModelForm):
    """Simple comment form"""
    
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
                'required': True
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts...',
                'required': True
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        
        if len(content) < 10:
            raise ValidationError("Comment must be at least 10 characters long.")
        
        if len(content) > 1000:
            raise ValidationError("Comment cannot exceed 1000 characters.")
        
        return content


class NewsFilterForm(forms.Form):
    """Basic filtering for news list"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search articles...'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=NewsCategory.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    article_type = forms.ChoiceField(
        choices=[('', 'All Types')] + NewsArticle.ARTICLE_TYPES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


# Admin-only forms (if you need them later)
class NewsArticleAdminForm(forms.ModelForm):
    """Simplified admin form for news articles"""
    
    class Meta:
        model = NewsArticle
        fields = [
            'title', 'article_type', 'category', 'excerpt', 'content',
            'featured_image', 'status', 'is_featured', 'is_breaking'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': CKEditor5Widget(config_name='default'),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        
        if len(title) < 10:
            raise ValidationError("Title must be at least 10 characters long.")
        
        return title
