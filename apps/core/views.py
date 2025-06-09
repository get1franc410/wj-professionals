# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\core\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg, Count
from django.utils import timezone
from .models import Company, Service, Testimonial, FAQ, ServiceCategory
from apps.news.models import NewsArticle
from apps.portfolio.models import Client
from apps.staff.models import Staff
from apps.reviews.models import Review  
from django.db.models import Avg, Count




def home_view(request):
    """Home page view with all necessary data"""
    company = Company.objects.first()

    review_stats = Review.objects.filter(status='approved').aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    
    # Get featured reviews (approved and featured)
    featured_reviews = Review.objects.filter(
        status='approved', 
        is_featured=True
    ).order_by('-created_at')[:6]

    tax_calculators = [
        {
            'name': 'PAYE Calculator',
            'description': 'Calculate personal income tax',
            'icon': 'fas fa-calculator',
            'url': 'https://www.firs.gov.ng/tax-calculator/'
        },
        {
            'name': 'VAT Calculator',
            'description': 'Calculate VAT on goods/services',
            'icon': 'fas fa-percentage',
            'url': 'https://www.firs.gov.ng/vat-calculator/'
        },
        {
            'name': 'WHT Calculator',
            'description': 'Calculate withholding tax',
            'icon': 'fas fa-receipt',
            'url': 'https://www.firs.gov.ng/withholding-tax-calculator/'
        },
        {
            'name': 'CIT Calculator',
            'description': 'Calculate company income tax',
            'icon': 'fas fa-building',
            'url': 'https://www.firs.gov.ng/company-tax-calculator/'
        }
    ]
    
    context = {
        'company': company,
        'featured_services': Service.objects.filter(is_featured=True, is_active=True)[:6],
        'all_services': Service.objects.filter(is_active=True)[:8],
        'recent_news': NewsArticle.objects.filter(status='published', publish_date__lte=timezone.now()).order_by('-publish_date')[:3],
        'featured_clients': Client.objects.filter(is_featured=True, is_public=True)[:6] if 'apps.portfolio' in settings.INSTALLED_APPS else [],
        'testimonials': Testimonial.objects.filter(is_featured=True, is_approved=True)[:3],
        'team_members': Staff.objects.filter(is_public=True, is_featured=True)[:4],
        'tax_calculators': tax_calculators,
        'review_stats': review_stats,
        'featured_reviews': featured_reviews,
        'overall_rating': review_stats['avg_rating'] or 4.7,
        'total_reviews': review_stats['total_reviews'] or 48,
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    """About page view"""
    company = Company.objects.first()

    review_stats = Review.objects.filter(status='approved').aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    
    # Rating sources (you can make this dynamic later)
    rating_sources = [
        {'name': 'Google Reviews', 'rating': 4.8, 'count': review_stats['total_reviews'] or 14},
        {'name': 'Client Portal', 'rating': 4.6, 'count': max(0, (review_stats['total_reviews'] or 32) - 5)},
        {'name': 'Direct Feedback', 'rating': 4.7, 'count': max(0, (review_stats['total_reviews'] or 17) - 10)},
    ]
    
    # ✅ FIXED: Enhanced achievements list
    achievements = [
        {'year': '2010', 'title': 'Company Founded', 'description': 'WJ Professionals was established with a vision to provide world-class accounting services.'},
        {'year': '2013', 'title': '100+ Clients', 'description': 'Reached milestone of 100 satisfied clients'},
        {'year': '2015', 'title': 'Major Expansion', 'description': 'Expanded services to include tax advisory and business consulting.'},
        {'year': '2017', 'title': 'Lagos Office', 'description': 'Opened branch office in Lagos'},
        {'year': '2018', 'title': 'Technology Integration', 'description': 'Implemented cloud-based accounting solutions for better client service.'},
        {'year': '2020', 'title': 'Digital Transformation', 'description': 'Launched online client portal and remote service capabilities.'},
        {'year': '2023', 'title': '500+ Clients', 'description': 'Expanded to serve over 500 clients nationwide'},
        {'year': '2024', 'title': 'Industry Recognition', 'description': 'Recognized as one of the leading accounting firm in Nigeria.'},
    ]
    
    context = {
        'company': company,
        'team_members': Staff.objects.filter(is_public=True, is_active=True),
        'achievements': achievements,
        'stats': {
            'years_experience': company.years_of_experience if company else 0,
            'clients_served': company.clients_served if company else 500,
            'projects_completed': company.projects_completed if company else 1200,
            'team_members': Staff.objects.filter(is_active=True).count(),
        },
        # ✅ FIXED: Pass review data separately in context
        'review_stats': review_stats,
        'overall_rating': review_stats['avg_rating'] or 4.7,
        'total_reviews': review_stats['total_reviews'] or 48,
        'rating_sources': rating_sources,
    }
    return render(request, 'core/about.html', context)

class ServiceListView(ListView):
    model = Service
    template_name = 'core/services.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).select_related('category')
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        
        if category:
            # Filter by category slug (since your ServiceCategory has slug field)
            queryset = queryset.filter(category__slug=category)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(short_description__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        return queryset.order_by('order', 'title')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all active categories for the filter menu
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('order', 'name')
        
        # Add current filter values
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        # Add category statistics
        context['category_stats'] = {}
        for category in context['categories']:
            context['category_stats'][category.slug] = Service.objects.filter(
                category=category, 
                is_active=True
            ).count()
        
        # Add total services count
        context['total_services'] = Service.objects.filter(is_active=True).count()
        
        # Add featured services
        context['featured_services'] = Service.objects.filter(
            is_active=True, 
            is_featured=True
        ).order_by('order')[:3]
        
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'core/service_detail.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(
            category=self.object.category, 
            is_active=True
        ).exclude(id=self.object.id)[:3]
        context['testimonials'] = Testimonial.objects.filter(is_approved=True)[:2]
        return context
    
def tax_calculator_view(request):
    """Tax Calculator page with links to official government calculators"""
    
    # Official Government Tax Calculators
    tax_calculators = [
        # FIRS (Federal Inland Revenue Service) Calculators
        {
            'name': 'FIRS Personal Income Tax Calculator',
            'description': 'Official FIRS calculator for personal income tax computation',
            'url': 'https://www.firs.gov.ng/tax-calculator/',
            'type': 'Personal Tax',
            'provider': 'Federal Inland Revenue Service (FIRS)',
            'is_official': True,
            'logo': 'images/logos/firs-logo.png'
        },
        {
            'name': 'FIRS Company Income Tax Calculator',
            'description': 'Calculate company income tax using official FIRS rates and guidelines',
            'url': 'https://www.firs.gov.ng/company-tax-calculator/',
            'type': 'Corporate Tax',
            'provider': 'Federal Inland Revenue Service (FIRS)',
            'is_official': True,
            'logo': 'images/logos/firs-logo.png'
        },
        {
            'name': 'FIRS VAT Calculator',
            'description': 'Official Value Added Tax calculator with current 7.5% rate',
            'url': 'https://www.firs.gov.ng/vat-calculator/',
            'type': 'VAT',
            'provider': 'Federal Inland Revenue Service (FIRS)',
            'is_official': True,
            'logo': 'images/logos/firs-logo.png'
        },
        {
            'name': 'FIRS Withholding Tax Calculator',
            'description': 'Calculate withholding tax for various transaction types',
            'url': 'https://www.firs.gov.ng/withholding-tax-calculator/',
            'type': 'Withholding Tax',
            'provider': 'Federal Inland Revenue Service (FIRS)',
            'is_official': True,
            'logo': 'images/logos/firs-logo.png'
        },
        
        # FCT Internal Revenue Service
        {
            'name': 'FCT IRS Personal Income Tax Calculator',
            'description': 'FCT-specific personal income tax calculator for Abuja residents',
            'url': 'https://www.fct-irs.gov.ng/tax-calculator/',
            'type': 'Personal Tax',
            'provider': 'FCT Internal Revenue Service',
            'is_official': True,
            'logo': 'images/logos/fct-irs-logo.png'
        },
        {
            'name': 'FCT IRS Property Tax Calculator',
            'description': 'Calculate property tax for FCT properties',
            'url': 'https://www.fct-irs.gov.ng/property-tax-calculator/',
            'type': 'Property Tax',
            'provider': 'FCT Internal Revenue Service',
            'is_official': True,
            'logo': 'images/logos/fct-irs-logo.png'
        },
        
        # Lagos State Internal Revenue Service
        {
            'name': 'LIRS Personal Income Tax Calculator',
            'description': 'Lagos State personal income tax calculator with state-specific rates',
            'url': 'https://www.etax.lirs.net',
            'type': 'Personal Tax',
            'provider': 'Lagos State Internal Revenue Service (LIRS)',
            'is_official': True,
            'logo': 'images/logos/lirs-logo.png'
        },
        {
            'name': 'LIRS Property Tax Calculator',
            'description': 'Calculate Lagos State property tax and land use charge',
            'url': 'https://www.etax.lirs.net',
            'type': 'Property Tax',
            'provider': 'Lagos State Internal Revenue Service (LIRS)',
            'is_official': True,
            'logo': 'images/logos/lirs-logo.png'
        },
        {
            'name': 'LIRS Business Premises Registration Calculator',
            'description': 'Calculate business premises registration fees for Lagos State',
            'url': 'https://www.etax.lirs.net',
            'type': 'Business Tax',
            'provider': 'Lagos State Internal Revenue Service (LIRS)',
            'is_official': True,
            'logo': 'images/logos/lirs-logo.png'
        },
        
        # Rivers State Internal Revenue Service
        {
            'name': 'RIRS Personal Income Tax Calculator',
            'description': 'Rivers State personal income tax calculator',
            'url': 'https://www.rirs.gov.ng/tax-calculator/',
            'type': 'Personal Tax',
            'provider': 'Rivers State Internal Revenue Service (RIRS)',
            'is_official': True,
            'logo': 'images/logos/rirs-logo.png'
        },
        
        # Kano State Internal Revenue Service
        {
            'name': 'KIRS Tax Calculator',
            'description': 'Kano State comprehensive tax calculator',
            'url': 'https://www.kirs.gov.ng/calculator/',
            'type': 'Personal Tax',
            'provider': 'Kano State Internal Revenue Service (KIRS)',
            'is_official': True,
            'logo': 'images/logos/kirs-logo.png'
        },
        
        # Ogun State Internal Revenue Service
        {
            'name': 'OGIRS Tax Calculator',
            'description': 'Ogun State personal and business tax calculator',
            'url': 'https://www.ogirs.gov.ng/tax-calculator/',
            'type': 'Personal Tax',
            'provider': 'Ogun State Internal Revenue Service (OGIRS)',
            'is_official': True,
            'logo': 'images/logos/ogirs-logo.png'
        },
        
        # Additional Professional Calculators
        {
            'name': 'CITN Tax Calculator',
            'description': 'Chartered Institute of Taxation of Nigeria professional calculator',
            'url': 'https://www.citn.org.ng/tax-calculator/',
            'type': 'Professional Tool',
            'provider': 'Chartered Institute of Taxation of Nigeria (CITN)',
            'is_official': False,
            'logo': 'images/logos/citn-logo.png'
        },
        {
            'name': 'ICAN Tax Guide Calculator',
            'description': 'Institute of Chartered Accountants tax computation guide',
            'url': 'https://www.icanig.org/tax-calculator/',
            'type': 'Professional Tool',
            'provider': 'Institute of Chartered Accountants of Nigeria (ICAN)',
            'is_official': False,
            'logo': 'images/logos/ican-logo.png'
        },
        
        # Pension and Social Security
        {
            'name': 'PenCom Pension Calculator',
            'description': 'Calculate pension contributions and benefits',
            'url': 'https://www.pencom.gov.ng/pension-calculator/',
            'type': 'Pension',
            'provider': 'National Pension Commission (PenCom)',
            'is_official': True,
            'logo': 'images/logos/pencom-logo.png'
        },
        {
            'name': 'NSITF Contribution Calculator',
            'description': 'Calculate NSITF (ECOWAS) contributions',
            'url': 'https://www.nsitf.gov.ng/calculator/',
            'type': 'Social Security',
            'provider': 'Nigeria Social Insurance Trust Fund (NSITF)',
            'is_official': True,
            'logo': 'images/logos/nsitf-logo.png'
        }
    ]
    
    # Group calculators by type
    calculator_types = list(set([calc['type'] for calc in tax_calculators]))
    calculator_types.sort()
    
    # Separate official vs professional tools
    official_calculators = [calc for calc in tax_calculators if calc.get('is_official', False)]
    professional_calculators = [calc for calc in tax_calculators if not calc.get('is_official', False)]
    
    context = {
        'company': Company.objects.first(),
        'tax_calculators': tax_calculators,
        'official_calculators': official_calculators,
        'professional_calculators': professional_calculators,
        'calculator_types': calculator_types,
        'total_calculators': len(tax_calculators),
        'official_count': len(official_calculators),
        'professional_count': len(professional_calculators)
    }
    return render(request, 'core/tax_calculator.html', context)

def faq_view(request):
    """FAQ page"""
    context = {
        'faqs': FAQ.objects.filter(is_active=True),
        'categories': FAQ.objects.filter(is_active=True).values_list('category', flat=True).distinct(),
    }
    return render(request, 'core/faq.html', context)

def search_view(request):
    """Global search functionality"""
    query = request.GET.get('q', '')
    results = {}
    
    if query:
        # Search services
        results['services'] = Service.objects.filter(
            Q(title__icontains=query) | 
            Q(short_description__icontains=query),
            is_active=True
        )[:5]
        
        # Search news
        results['news'] = NewsArticle.objects.filter(
            Q(title__icontains=query) | 
            Q(excerpt__icontains=query),
            status='published'
        )[:5]
        
        # Search documents
        from apps.documents.models import Document
        results['documents'] = Document.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query),
            is_active=True,
            access_level='public'
        )[:5]
    
    context = {
        'query': query,
        'results': results,
        'total_results': sum(len(result) for result in results.values())
    }
    return render(request, 'core/search_results.html', context)

def admin_access(request):
    """Hidden admin access page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'core/admin_access.html')

@login_required
def admin_logout(request):
    """Admin logout"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('core:home')