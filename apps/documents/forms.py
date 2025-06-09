# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\documents\forms.py
"""
Documents Forms
===============
Forms for document management, upload, and filtering
"""

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_ckeditor_5.widgets import CKEditor5Widget
import os

from .models import Document, DocumentCategory, DownloadLog


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading documents"""
    
    class Meta:
        model = Document
        fields = [
            'title', 'description', 'file', 'category', 'access_level',
            'requires_approval', 'is_active', 'is_featured', 'tags',
            'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter document title',
                'required': True
            }),
            'description': CKEditor5Widget(attrs={
                'class': 'form-control',
                'placeholder': 'Enter document description'
            }, config_name='default'),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.rtf',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'access_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'requires_approval': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas (e.g., tax, business, guide)',
                'data-role': 'tagsinput'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'SEO meta description (optional)',
                'maxlength': 160
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = DocumentCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Select a category"
        
        # Help texts
        self.fields['title'].help_text = "Choose a clear, descriptive title"
        self.fields['file'].help_text = "Supported formats: PDF, Word, Excel, PowerPoint, Text files (Max: 50MB)"
        self.fields['access_level'].help_text = "Who can access this document"
        self.fields['requires_approval'].help_text = "Require admin approval before download"
        self.fields['tags'].help_text = "Tags help users find your document"
        
        # Set initial values
        self.fields['is_active'].initial = True
        self.fields['access_level'].initial = 'public'

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 50MB)
            max_size = 50 * 1024 * 1024  # 50MB in bytes
            if file.size > max_size:
                raise ValidationError(f"File size cannot exceed 50MB. Current size: {file.size / (1024*1024):.1f}MB")
            
            # Check file extension
            allowed_extensions = [
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', 
                '.ppt', '.pptx', '.txt', '.rtf'
            ]
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    f"File type '{file_extension}' not supported. "
                    f"Allowed types: {', '.join(allowed_extensions)}"
                )
            
            # Check for malicious file names
            if any(char in file.name for char in ['..', '/', '\\']):
                raise ValidationError("Invalid file name.")
        
        return file

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            # Convert comma-separated string to list
            tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
            # Remove duplicates and limit to 10 tags
            tag_list = list(dict.fromkeys(tag_list))[:10]
            return tag_list
        return []

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            # Check for duplicate titles in the same category
            category = self.cleaned_data.get('category')
            if category:
                queryset = Document.objects.filter(title=title, category=category)
                if self.instance.pk:
                    queryset = queryset.exclude(pk=self.instance.pk)
                if queryset.exists():
                    raise ValidationError("A document with this title already exists in this category.")
        return title


class DocumentEditForm(DocumentUploadForm):
    """Form for editing existing documents"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make file field optional for editing
        self.fields['file'].required = False
        self.fields['file'].help_text = "Leave empty to keep current file. Upload new file to replace."


class DocumentFilterForm(forms.Form):
    """Form for filtering documents"""
    
    SORT_CHOICES = [
        ('', 'Default'),
        ('-created_at', 'Newest First'),
        ('created_at', 'Oldest First'),
        ('title', 'Title A-Z'),
        ('-title', 'Title Z-A'),
        ('-download_count', 'Most Downloaded'),
        ('-view_count', 'Most Viewed'),
        ('file_size', 'Smallest First'),
        ('-file_size', 'Largest First'),
    ]
    
    FILE_TYPE_CHOICES = [
        ('', 'All Types'),
        ('.pdf', 'PDF'),
        ('.doc', 'Word Document'),
        ('.docx', 'Word Document (New)'),
        ('.xls', 'Excel Spreadsheet'),
        ('.xlsx', 'Excel Spreadsheet (New)'),
        ('.ppt', 'PowerPoint'),
        ('.pptx', 'PowerPoint (New)'),
        ('.txt', 'Text File'),
        ('.rtf', 'Rich Text'),
    ]
    
    search = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search documents...',
            'autocomplete': 'off'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    file_type = forms.ChoiceField(
        choices=FILE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    access_level = forms.ChoiceField(
        choices=[('', 'All Access Levels')] + Document.ACCESS_LEVELS,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    is_featured = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Featured Only"
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="From Date"
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="To Date"
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise ValidationError("Start date cannot be after end date.")
        
        return cleaned_data


class DocumentCategoryForm(forms.ModelForm):
    """Form for creating/editing document categories"""
    
    class Meta:
        model = DocumentCategory
        fields = ['name', 'description', 'icon', 'color', 'is_active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name',
                'required': True
            }),
            'description': CKEditor5Widget(attrs={
                'class': 'form-control',
                'placeholder': 'Category description'
            }, config_name='default'),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'FontAwesome icon class (e.g., fas fa-folder)',
                'data-toggle': 'tooltip',
                'title': 'Use FontAwesome icon classes'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'title': 'Choose category color'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 1
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['icon'].initial = 'fas fa-folder'
        self.fields['color'].initial = '#007bff'
        self.fields['is_active'].initial = True
        self.fields['order'].initial = 0
        
        # Help texts
        self.fields['name'].help_text = "Choose a clear, descriptive name"
        self.fields['icon'].help_text = "FontAwesome icon class (visit fontawesome.com for icons)"
        self.fields['color'].help_text = "Color for category identification"
        self.fields['order'].help_text = "Display order (lower numbers appear first)"

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Check for duplicate names
            queryset = DocumentCategory.objects.filter(name__iexact=name)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise ValidationError("A category with this name already exists.")
        return name

    def clean_icon(self):
        icon = self.cleaned_data.get('icon', '')
        if icon and not icon.startswith(('fa', 'fas', 'far', 'fab')):
            raise ValidationError("Icon should be a valid FontAwesome class (e.g., 'fas fa-folder')")
        return icon

    def clean_color(self):
        color = self.cleaned_data.get('color', '')
        if color and not color.startswith('#'):
            raise ValidationError("Color should be a valid hex color code (e.g., '#007bff')")
        if len(color) not in [4, 7]:  # #fff or #ffffff
            raise ValidationError("Invalid color format. Use #fff or #ffffff format.")
        return color


class BulkDocumentActionForm(forms.Form):
    """Form for bulk actions on documents"""
    
    ACTION_CHOICES = [
        ('', 'Select action...'),
        ('activate', 'Activate selected'),
        ('deactivate', 'Deactivate selected'),
        ('feature', 'Mark as featured'),
        ('unfeature', 'Remove from featured'),
        ('delete', 'Delete selected'),
        ('change_category', 'Change category'),
        ('change_access', 'Change access level'),
        ('export', 'Export list'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    selected_documents = forms.CharField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    # Additional fields for specific actions
    new_category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    new_access_level = forms.ChoiceField(
        choices=Document.ACCESS_LEVELS,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    def clean_selected_documents(self):
        documents = self.cleaned_data.get('selected_documents', '')
        if not documents:
            raise ValidationError("No documents selected.")
        
        try:
            document_ids = [int(x) for x in documents.split(',') if x.strip()]
            if not document_ids:
                raise ValidationError("No valid documents selected.")
            
            # Verify documents exist
            existing_count = Document.objects.filter(id__in=document_ids).count()
            if existing_count != len(document_ids):
                raise ValidationError("Some selected documents no longer exist.")
            
            return document_ids
        except ValueError:
            raise ValidationError("Invalid document selection.")

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        
        if action == 'change_category' and not cleaned_data.get('new_category'):
            raise ValidationError("Please select a new category.")
        
        if action == 'change_access' and not cleaned_data.get('new_access_level'):
            raise ValidationError("Please select a new access level.")
        
        return cleaned_data


class DocumentRequestForm(forms.Form):
    """Form for requesting specific documents"""
    
    URGENCY_CHOICES = [
        ('low', 'Low - Within a week'),
        ('medium', 'Medium - Within 3 days'),
        ('high', 'High - Within 24 hours'),
        ('urgent', 'Urgent - ASAP'),
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
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone number (optional)'
        })
    )
    
    document_title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'What document are you looking for?',
            'required': True
        })
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Please describe the document you need and how you plan to use it...',
            'required': True
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(is_active=True),
        required=False,
        empty_label="Select category (if known)",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    urgency = forms.ChoiceField(
        choices=URGENCY_CHOICES,
        initial='medium',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    additional_info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any additional information that might help us find or create the document...'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add any custom email validation here
        return email


class DocumentSearchForm(forms.Form):
    """Advanced search form for documents"""
    
    query = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Search documents, descriptions, tags...',
            'autocomplete': 'off'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add search suggestions or autocomplete functionality here
        pass

    def get_search_results(self):
        """Return search results based on form data"""
        query = self.cleaned_data.get('query', '').strip()
        
        if not query:
            return Document.objects.none()
        
        from django.db.models import Q
        
        # Build search query
        search_query = Q()
        
        # Search in title, description, and tags
        search_terms = query.split()
        for term in search_terms:
            search_query |= (
                Q(title__icontains=term) |
                Q(description__icontains=term) |
                Q(tags__icontains=term) |
                Q(meta_description__icontains=term)
            )
        
        return Document.objects.filter(
            search_query,
            is_active=True,
            access_level='public'
        ).distinct().order_by('-created_at')

