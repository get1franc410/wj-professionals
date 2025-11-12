# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\reviews\forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'client_name', 'client_email', 'client_company', 
            'client_position', 'rating', 'title', 'review_text', 'service_used'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'client_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your company name (optional)'
            }),
            'client_position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your position (optional)'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief title for your review'
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your experience with our services...'
            }),
            'service_used': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Which service did you use? (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add required field indicators
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True
                if 'placeholder' in field.widget.attrs:
                    field.widget.attrs['placeholder'] += ' *'
