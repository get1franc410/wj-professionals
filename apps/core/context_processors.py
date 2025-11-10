# apps/core/context_processors.py
from apps.core.models import Company
from apps.core.fixtures.company_data import COMPANY_DATA, TEMPLATE_DEFAULTS
from django.utils import timezone

def company_info(request):
    """
    Add company information to all templates
    Priority: Database > Fixtures > Hardcoded defaults
    """
    try:
        # 1. Try to get from database first
        company = Company.objects.first()
        
        if company:
            # ✅ Database data available - use it
            return {'company': company}
        
        # 2. No database data - use fixtures
        company_data = COMPANY_DATA.copy()
        
        # Calculate years of experience automatically
        if company_data.get('years_experience_calculated'):
            current_year = timezone.now().year
            company_data['years_of_experience'] = current_year - company_data.get('established_year', 2010)
            company_data['years_experience'] = company_data['years_of_experience']  # Alias
        
        # Create a mock company object with fixture data
        return {'company': type('Company', (), company_data)()}
        
    except Exception as e:
        # 3. Fallback to basic defaults
        return {'company': type('Company', (), TEMPLATE_DEFAULTS)()}

def portfolio_stats(request):
    """Add portfolio stats to all templates"""
    try:
        # Try to get from company model first
        company = Company.objects.first()
        if company:
            return {
                'portfolio_stats': {
                    'total_clients': company.clients_served,
                    'projects_completed': company.projects_completed,
                    'years_experience': company.years_of_experience,
                    'success_rate': 98,  # Could be calculated or stored
                    'industries_served': 25,  # Could be calculated from portfolio
                }
            }
    except:
        pass
    
    # Fallback to fixture data
    return {
        'portfolio_stats': {
            'total_clients': COMPANY_DATA.get('clients_served', 500),
            'projects_completed': COMPANY_DATA.get('projects_completed', 1200),
            'years_experience': timezone.now().year - COMPANY_DATA.get('established_year', 2010),
            'success_rate': 98,
            'industries_served': 25,
        }
    }
