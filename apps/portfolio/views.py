# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\portfolio\views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.db.models import Q
from .models import Client, Industry, CaseStudy

class ClientPortfolioView(ListView):
    model = Client
    template_name = 'portfolio/client_list.html'
    context_object_name = 'clients'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Client.objects.filter(is_public=True)
        industry = self.request.GET.get('industry')
        client_type = self.request.GET.get('type')
        search = self.request.GET.get('search')
        
        if industry:
            queryset = queryset.filter(industry_id=industry)
        
        if client_type:
            queryset = queryset.filter(client_type=client_type)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(project_title__icontains=search) |
                Q(project_description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industries'] = Industry.objects.filter(is_active=True)
        context['client_types'] = Client.CLIENT_TYPES
        context['featured_clients'] = Client.objects.filter(
            is_featured=True, 
            is_public=True
        )[:6]
        context['selected_industry'] = self.request.GET.get('industry', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        # Portfolio statistics
        context['stats'] = {
            'total_clients': Client.objects.filter(is_public=True).count(),
            'industries_served': Industry.objects.filter(
                client__is_public=True
            ).distinct().count(),
            'ongoing_projects': Client.objects.filter(
                project_status='ongoing', 
                is_public=True
            ).count(),
            'completed_projects': Client.objects.filter(
                project_status='completed', 
                is_public=True
            ).count(),
        }
        return context

class ClientDetailView(DetailView):
    model = Client
    template_name = 'portfolio/client_detail.html'
    context_object_name = 'client'
    
    def get_queryset(self):
        return Client.objects.filter(is_public=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_images'] = self.object.project_images.all()
        context['related_clients'] = Client.objects.filter(
            industry=self.object.industry,
            is_public=True
        ).exclude(id=self.object.id)[:3]
        
        # Check if case study exists
        try:
            context['case_study'] = self.object.case_study
        except CaseStudy.DoesNotExist:
            context['case_study'] = None
        
        return context

def industry_view(request, industry_id):
    """View clients by industry"""
    industry = get_object_or_404(Industry, id=industry_id, is_active=True)
    clients = Client.objects.filter(
        industry=industry,
        is_public=True
    )
    
    context = {
        'industry': industry,
        'clients': clients,
        'client_count': clients.count(),
    }
    return render(request, 'portfolio/industry_detail.html', context)

def case_studies_view(request):
    """List all published case studies"""
    case_studies = CaseStudy.objects.filter(
        is_published=True,
        client__is_public=True
    ).select_related('client')
    
    context = {
        'case_studies': case_studies,
    }
    return render(request, 'portfolio/case_studies.html', context)

def case_study_detail_view(request, client_id):
    """Detailed case study view"""
    client = get_object_or_404(Client, id=client_id, is_public=True)
    
    try:
        case_study = client.case_study
        if not case_study.is_published:
            raise Http404("Case study not found")
    except CaseStudy.DoesNotExist:
        raise Http404("Case study not found")
    
    context = {
        'client': client,
        'case_study': case_study,
        'related_case_studies': CaseStudy.objects.filter(
            is_published=True,
            client__industry=client.industry,
            client__is_public=True
        ).exclude(client=client)[:3]
    }
    return render(request, 'portfolio/case_study_detail.html', context)
