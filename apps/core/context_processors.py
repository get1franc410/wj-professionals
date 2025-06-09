# apps/core/context_processors.py
from apps.core.models import Company
from apps.core.fixtures.company_data import COMPANY_DATA

def company_info(request):
    """Add company information to all templates"""
    try:
        # Get company from database
        company = Company.objects.first()
        
        # If no company in database, use fixture data
        if not company:
            company_data = COMPANY_DATA.copy()
            # Calculate years of experience
            from django.utils import timezone
            current_year = timezone.now().year
            company_data['years_of_experience'] = current_year - company_data.get('established_year', 2010)
            return {'company': type('Company', (), company_data)()}
        
        return {'company': company}
    except Exception:
        # Fallback to fixture data
        company_data = COMPANY_DATA.copy()
        from django.utils import timezone
        current_year = timezone.now().year
        company_data['years_of_experience'] = current_year - company_data.get('established_year', 2010)
        return {'company': type('Company', (), company_data)()}

def portfolio_stats(request):
    """Add portfolio stats to all templates"""
    try:
        # Try to get stats from database if you have a model
        from .models import PortfolioStats
        stats = PortfolioStats.objects.first()
        if stats:
            return {'portfolio_stats': stats}
    except:
        pass
    
    # Default values
    default_stats = {
        'total_clients': 520,
        'industries_served': 25,
        'projects_completed': 1200,
        'success_rate': 98
    }
    
    return {'portfolio_stats': type('Stats', (), default_stats)()}