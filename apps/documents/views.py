# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\documents\views.py
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from django.utils import timezone
from apps.documents.models import Document, DocumentCategory, DownloadLog
import mimetypes
import os

class DocumentListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Document.objects.filter(is_active=True, access_level='public')
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        file_type = self.request.GET.get('type')
        
        if category:
            try:
                category_obj = DocumentCategory.objects.get(slug=category, is_active=True)
                queryset = queryset.filter(category=category_obj)
            except DocumentCategory.DoesNotExist:
                # If slug doesn't exist, try by ID as fallback
                try:
                    queryset = queryset.filter(category_id=int(category))
                except (ValueError, TypeError):
                    pass 
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        
        return queryset.select_related('category').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add document count for each category
        categories = DocumentCategory.objects.filter(is_active=True).prefetch_related('document_set')
        for category in categories:
            category.document_count = category.document_set.filter(
                is_active=True, 
                access_level='public'
            ).count()
        
        context['categories'] = categories
        context['file_types'] = Document.objects.filter(
            is_active=True, 
            access_level='public'
        ).values_list('file_type', flat=True).distinct()
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['featured_documents'] = Document.objects.filter(
            is_featured=True, 
            is_active=True, 
            access_level='public'
        ).select_related('category')[:3]
        return context

def document_detail_view(request, document_id):
    """Document detail view with download tracking"""
    document = get_object_or_404(
        Document, 
        id=document_id, 
        is_active=True, 
        access_level='public'
    )
    
    # Increment view count
    Document.objects.filter(id=document_id).update(view_count=F('view_count') + 1)
    
    # Get related documents
    related_documents = Document.objects.filter(
        category=document.category,
        is_active=True,
        access_level='public'
    ).exclude(id=document_id)[:3]
    
    context = {
        'document': document,
        'related_documents': related_documents,
    }
    return render(request, 'documents/document_detail.html', context)

def download_document(request, document_id):
    """Handle document downloads with logging"""
    document = get_object_or_404(
        Document, 
        id=document_id, 
        is_active=True
    )
    
    # Check access permissions
    if document.access_level == 'staff' and not request.user.is_staff:
        raise Http404("Document not found")
    elif document.access_level == 'admin' and not request.user.is_superuser:
        raise Http404("Document not found")
    elif document.access_level == 'registered' and not request.user.is_authenticated:
        messages.error(request, "Please login to download this document.")
        return redirect('login')
    
    # Log the download
    DownloadLog.objects.create(
        document=document,
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Increment download count
    Document.objects.filter(id=document_id).update(download_count=F('download_count') + 1)
    
    # Serve the file
    file_path = document.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0])
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    
    raise Http404("File not found")

@login_required
def upload_document_view(request):
    """Staff upload document view"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to upload documents.")
        return redirect('home')
    
    if request.method == 'POST':
        from .forms import DocumentUploadForm
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, "Document uploaded successfully!")
            return redirect('documents:document_list')
    else:
        from .forms import DocumentUploadForm
        form = DocumentUploadForm()
    
    context = {'form': form}
    return render(request, 'documents/upload.html', context)

def category_view(request, category_id):
    """View documents by category"""
    category = get_object_or_404(DocumentCategory, id=category_id, is_active=True)
    documents = Document.objects.filter(
        category=category,
        is_active=True,
        access_level='public'
    )
    
    context = {
        'category': category,
        'documents': documents,
    }
    return render(request, 'documents/category_detail.html', context)
