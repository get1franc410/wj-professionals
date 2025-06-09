# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\core\management\commands\load_sample_data.py
"""
Management Command to Load Sample Data
=====================================
Django management command to populate the database with sample data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.base import ContentFile
import os  
from django.conf import settings  
from django.core.files import File 

from apps.core.models import Company, Service, ServiceCategory, Position, Testimonial, FAQ
from apps.staff.models import Staff, Department
from apps.news.models import NewsArticle, NewsCategory

class Command(BaseCommand):
    help = 'Load sample data into the database'


    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        self.stdout.write('Loading sample data...')
        
        # Load data in order
        self.load_company_data()
        self.load_service_categories()
        self.load_services()
        # self.load_departments()
        self.load_staff()
        self.load_news_categories()
        self.load_news_articles()
        self.load_testimonials()
        self.load_faqs()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )

    def clear_data(self):
        """Clear existing data"""
        self.stdout.write('Clearing existing data...')
        
        # Clear in reverse dependency order
        FAQ.objects.all().delete()
        self.stdout.write('Cleared FAQ data')
        
        Testimonial.objects.all().delete()
        self.stdout.write('Cleared Testimonial data')
        
        NewsArticle.objects.all().delete()
        self.stdout.write('Cleared NewsArticle data')
        
        NewsCategory.objects.all().delete()
        self.stdout.write('Cleared NewsCategory data')
        
        Staff.objects.all().delete()
        self.stdout.write('Cleared Staff data')
        
        Department.objects.all().delete()
        self.stdout.write('Cleared Department data')
        
        Service.objects.all().delete()
        self.stdout.write('Cleared Service data')
        
        ServiceCategory.objects.all().delete()
        self.stdout.write('Cleared ServiceCategory data')
        
        Company.objects.all().delete()
        self.stdout.write('Cleared Company data')

    def load_company_data(self):
        """Load company information from centralized company_data.py"""
        self.stdout.write('🏢 Loading company data from centralized source...')
        
        # Import the centralized company data
        from apps.core.fixtures.company_data import COMPANY_DATA
        
        # Prepare data for model creation
        company_data = {
            'name': COMPANY_DATA['name'],
            'tagline': COMPANY_DATA['tagline'],
            'description': COMPANY_DATA['description'],
            'mission': COMPANY_DATA['mission'],
            'vision': COMPANY_DATA['vision'],
            'values': COMPANY_DATA.get('values', ''),
            'about_us': COMPANY_DATA.get('about_us', ''),
            
            # Contact Information
            'email': COMPANY_DATA.get('email', COMPANY_DATA.get('email_primary', 'info@wjprofessionals.com')),
            'phone': COMPANY_DATA.get('phone', COMPANY_DATA.get('phone_primary', '+234-803-065-5969')),
            
            # Address
            'address': COMPANY_DATA.get('address', 'Plot 123, Ademola Adetokunbo Crescent, Wuse II, Abuja, FCT'),
            'city': COMPANY_DATA.get('city', 'Abuja'),
            'state': COMPANY_DATA.get('state', 'Federal Capital Territory'),
            'country': COMPANY_DATA.get('country', 'Nigeria'),
            
            # Online Presence
            'website': COMPANY_DATA.get('website', 'https://www.wjprofessionals.com'),
            'linkedin': COMPANY_DATA.get('linkedin', ''),
            'twitter': COMPANY_DATA.get('twitter', ''),
            'facebook': COMPANY_DATA.get('facebook', ''),
            'instagram': COMPANY_DATA.get('instagram', ''),
            
            # Business Details - These are the KEY FIXES for your stats
            'established_year': COMPANY_DATA.get('established_year', 2010),
            'working_hours': COMPANY_DATA.get('working_hours', ''),
            'certifications': COMPANY_DATA.get('certifications', []),
            
            # Stats - THE IMPORTANT ONES FOR YOUR TEMPLATES
            'clients_served': COMPANY_DATA.get('clients_served', 500),
            'projects_completed': COMPANY_DATA.get('projects_completed', 1200),
        }
        
        company, created = Company.objects.get_or_create(
            name=company_data['name'],
            defaults=company_data
        )
        
        if created:
            self.stdout.write(f'  ✅ Created company: {company.name}')
            self.stdout.write(f'     📊 Clients Served: {company.clients_served}')
            self.stdout.write(f'     📊 Projects Completed: {company.projects_completed}')
            self.stdout.write(f'     📊 Years Experience: {company.years_of_experience}')
        else:
            # Update existing company with new data - IMPORTANT FOR FIXING STATS
            updated_fields = []
            for key, value in company_data.items():
                if hasattr(company, key):
                    old_value = getattr(company, key)
                    if old_value != value:
                        setattr(company, key, value)
                        updated_fields.append(key)
            
            if updated_fields:
                company.save()
                self.stdout.write(f'  🔄 Updated company: {company.name}')
                self.stdout.write(f'     📝 Updated fields: {", ".join(updated_fields)}')
            else:
                self.stdout.write(f'  ℹ️  Company data already up-to-date: {company.name}')
            
            # Always show current stats
            self.stdout.write(f'     📊 Current Stats:')
            self.stdout.write(f'        • Clients Served: {company.clients_served}')
            self.stdout.write(f'        • Projects Completed: {company.projects_completed}')
            self.stdout.write(f'        • Years Experience: {company.years_of_experience}')
        
        return company

    def load_service_categories(self):
        """Load comprehensive service categories using DRY approach"""
        self.stdout.write('📂 Loading service categories...')
        
        # Import from centralized data
        try:
            from apps.core.fixtures.services_data import SERVICE_CATEGORIES
            self.stdout.write(f'✅ Successfully imported {len(SERVICE_CATEGORIES)} categories from services_data.py')
        except ImportError as e:
            self.stdout.write(f'❌ Error importing service categories: {e}')
            # Fallback to inline categories
            SERVICE_CATEGORIES = [
                {
                    'name': 'Tax Services',
                    'slug': 'tax-services',
                    'description': 'Comprehensive tax preparation, planning, and compliance services',
                    'icon': 'fas fa-calculator',
                    'color': '#007bff',
                    'order': 1
                },
                {
                    'name': 'Audit & Assurance',
                    'slug': 'audit-assurance',
                    'description': 'Independent audit and assurance services',
                    'icon': 'fas fa-search-dollar',
                    'color': '#28a745',
                    'order': 2
                },
                {
                    'name': 'Business Advisory',
                    'slug': 'business-advisory',
                    'description': 'Strategic business consulting and advisory services',
                    'icon': 'fas fa-chart-line',
                    'color': '#dc3545',
                    'order': 3
                },
                {
                    'name': 'Accounting Services',
                    'slug': 'accounting-services',
                    'description': 'Professional accounting, bookkeeping, and financial management',
                    'icon': 'fas fa-file-invoice-dollar',
                    'color': '#6f42c1',
                    'order': 4
                },
                {
                    'name': 'Business Registration',
                    'slug': 'business-registration',
                    'description': 'Complete business incorporation and registration services',
                    'icon': 'fas fa-building',
                    'color': '#fd7e14',
                    'order': 5
                },
                {
                    'name': 'Specialized Services',
                    'slug': 'specialized-services',
                    'description': 'Forensic accounting, investigations, and specialized consulting',
                    'icon': 'fas fa-search-dollar',
                    'color': '#e83e8c',
                    'order': 6
                }
            ]
        
        created_count = updated_count = 0
        
        for cat_data in SERVICE_CATEGORIES:
            cat_data['is_active'] = cat_data.get('is_active', True)
            cat_data['order'] = cat_data.get('order', 1)
            
            obj, created = self.create_or_update_object(
                ServiceCategory, 'slug', cat_data['slug'], cat_data,
                update_fields=['name', 'description', 'icon', 'color', 'order', 'is_active']
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        self.log_creation_stats('Service Categories', created_count, updated_count)


    def load_services(self):
        """Load services from centralized services_data.py with enhanced data"""
        self.stdout.write('💼 Loading services from centralized data...')
        
        # Import from your existing services_data.py file
        try:
            from apps.core.fixtures.services_data import SERVICES_DATA
            self.stdout.write(f'✅ Successfully imported {len(SERVICES_DATA)} services from services_data.py')
        except ImportError as e:
            self.stdout.write(f'❌ Error importing services data: {e}')
            return
        
        import re
        
        created_count = 0
        updated_count = 0
        
        for service_data in SERVICES_DATA:
            try:
                # Get category by slug
                try:
                    category = ServiceCategory.objects.get(slug=service_data['category'])
                except ServiceCategory.DoesNotExist:
                    self.stdout.write(f'  ❌ Category not found: {service_data["category"]} for service: {service_data["title"]}')
                    continue
                
                # Extract starting price
                starting_price = service_data.get('starting_price', 0.00)
                
                # Convert features list to string if it's a list
                features_text = ''
                if 'features' in service_data:
                    if isinstance(service_data['features'], list):
                        features_text = '\n'.join(service_data['features'])
                    else:
                        features_text = service_data['features']
                
                # Prepare service model data
                service_model_data = {
                    'title': service_data['title'],
                    'category': category,
                    'short_description': service_data['short_description'],
                    'description': service_data.get('detailed_description', service_data['short_description']),
                    'starting_price': starting_price,
                    'features': features_text,
                    'delivery_time': service_data.get('duration', 'Contact for details'),
                    'is_featured': service_data.get('is_featured', False),
                    'is_active': True,
                    'meta_description': service_data['short_description'][:160],
                    'icon': service_data.get('icon', 'fas fa-cog'),
                }
                
                # Add additional fields if they exist in your Service model
                if hasattr(Service, 'is_popular'):
                    service_model_data['is_popular'] = service_data.get('is_popular', False)
                
                # Create or update service
                service, created = Service.objects.get_or_create(
                    slug=service_data['slug'],
                    defaults=service_model_data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'  ✅ Created: {service.title}')
                    self.stdout.write(f'     💰 Price: ₦{service.starting_price:,.2f}')
                    self.stdout.write(f'     📂 Category: {service.category.name}')
                    self.stdout.write(f'     ⏱️  Delivery: {service.delivery_time}')
                else:
                    # Update existing service
                    updated_fields = []
                    for key, value in service_model_data.items():
                        if hasattr(service, key) and key not in ['slug']:
                            old_value = getattr(service, key)
                            if old_value != value:
                                setattr(service, key, value)
                                updated_fields.append(key)
                    
                    if updated_fields:
                        service.save()
                        updated_count += 1
                        self.stdout.write(f'  🔄 Updated: {service.title} ({", ".join(updated_fields)})')
                    else:
                        self.stdout.write(f'  ℹ️  Already up-to-date: {service.title}')
                        
            except Exception as e:
                self.stdout.write(f'  ❌ Error creating service {service_data.get("title", "Unknown")}: {str(e)}')
        
        self.stdout.write(f'📊 Services - Created: {created_count}, Updated: {updated_count}')


    def load_departments(self):
        """Load departments"""
        self.stdout.write('🏢 Loading departments...')
        
        departments = [
            {
                'name': 'Tax Department',
                'slug': 'tax-department',
                'description': 'Handles all tax-related services and compliance',
                'email': 'tax@wjprofessionals.com',
                'phone': '+234-801-100-1001',
                'is_active': True,
                'order': 1
            },
            {
                'name': 'Advisory Services',
                'slug': 'advisory-services',
                'description': 'Business advisory and consulting services',
                'email': 'advisory@wjprofessionals.com',
                'phone': '+234-801-100-1002',
                'is_active': True,
                'order': 2
            },
            {
                'name': 'Audit Department',
                'slug': 'audit-department',
                'description': 'Independent audit and assurance services',
                'email': 'audit@wjprofessionals.com',
                'phone': '+234-801-100-1003',
                'is_active': True,
                'order': 3
            },
            {
                'name': 'Accounting Services',
                'slug': 'accounting-services',
                'description': 'Professional accounting and bookkeeping services',
                'email': 'accounting@wjprofessionals.com',
                'phone': '+234-801-100-1004',
                'is_active': True,
                'order': 4
            }
        ]
        
        for dept_data in departments:
            department, created = Department.objects.get_or_create(
                slug=dept_data['slug'], 
                defaults=dept_data
            )
            
            if created:
                self.stdout.write(f'  ✅ Created: {department.name}')

    def load_positions(self):
        """Load positions"""
        self.stdout.write('👔 Loading positions...')
        
        positions = [
            {
                'title': 'Senior Tax Consultant',
                'slug': 'senior-tax-consultant',
                'description': 'Senior level tax consulting position',
                'level': 'senior'
            },
            {
                'title': 'Business Advisor',
                'slug': 'business-advisor',
                'description': 'Business advisory and consulting role',
                'level': 'mid'
            },
            {
                'title': 'Managing Partner',
                'slug': 'managing-partner',
                'description': 'Executive leadership position',
                'level': 'executive'
            },
            {
                'title': 'Senior Auditor',
                'slug': 'senior-auditor',
                'description': 'Senior audit and assurance specialist',
                'level': 'senior'
            },
            {
                'title': 'Accounting Manager',
                'slug': 'accounting-manager',
                'description': 'Accounting and bookkeeping manager',
                'level': 'mid'
            }
        ]
        
        for pos_data in positions:
            position, created = Position.objects.get_or_create(
                slug=pos_data['slug'],
                defaults=pos_data
            )
            
            if created:
                self.stdout.write(f'  ✅ Created: {position.title}')

    def load_staff(self):
        """Load staff using centralized staff data with photo support"""
        self.stdout.write('👥 Loading staff from centralized data...')
        
        # Import the centralized staff data
        from apps.core.fixtures.staff_data import STAFF_DATA, DEPARTMENTS, POSITIONS
        from datetime import datetime, timedelta
        import random
        
        # Load positions first
        for pos_data in POSITIONS:
            position, created = Position.objects.get_or_create(
                slug=pos_data['slug'],
                defaults=pos_data
            )
            if created:
                self.stdout.write(f'  ✅ Created position: {position.title}')
        
        # Load departments WITHOUT head_of_department first
        departments_created = {}
        for dept_data in DEPARTMENTS:
            # Create department without head_of_department
            dept_data_copy = dept_data.copy()
            dept_data_copy.pop('head_of_department', None)  # Remove head_of_department
            
            department, created = Department.objects.get_or_create(
                slug=dept_data_copy['slug'],
                defaults=dept_data_copy
            )
            departments_created[dept_data['slug']] = department
            
            if created:
                self.stdout.write(f'  ✅ Created department: {department.name}')
        
        # Create staff members
        staff_created = {}
        for i, staff_data in enumerate(STAFF_DATA):
            try:
                # Create user first
                username = f"{staff_data['first_name'].lower()}.{staff_data['last_name'].lower()}"
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': staff_data['first_name'],
                        'last_name': staff_data['last_name'],
                        'email': staff_data['email'],
                        'is_staff': True
                    }
                )
                
                # 🔧 FIX: Update existing user if data is different
                if not created:
                    # Check if any data needs updating
                    needs_update = False
                    if user.first_name != staff_data['first_name']:
                        user.first_name = staff_data['first_name']
                        needs_update = True
                    if user.last_name != staff_data['last_name']:
                        user.last_name = staff_data['last_name']
                        needs_update = True
                    if user.email != staff_data['email']:
                        user.email = staff_data['email']
                        needs_update = True
                    
                    if needs_update:
                        user.save()
                        self.stdout.write(f'  🔄 Updated user: {user.get_full_name()}')
                    else:
                        self.stdout.write(f'  ℹ️  User already up-to-date: {user.get_full_name()}')
                else:
                    # New user created
                    user.set_password('staff123')
                    user.save()
                    self.stdout.write(f'  ✅ Created user: {user.get_full_name()}')
                
                # Get department
                department = departments_created[staff_data['department']]
                
                # Generate employee ID
                existing_count = Staff.objects.count()
                employee_id = f"WJ{existing_count + 1:03d}"
                
                # Generate a realistic date_joined (between 1-5 years ago)
                years_ago = random.randint(1, 5)
                months_ago = random.randint(0, 11)
                days_ago = random.randint(1, 28)
                date_joined = timezone.now() - timedelta(days=years_ago*365 + months_ago*30 + days_ago)
                
                # Create staff member with date_joined
                staff, staff_created_flag = Staff.objects.get_or_create(
                    user=user,
                    defaults={
                        'employee_id': employee_id,
                        'department': department,
                        'position': staff_data['position'],
                        'bio': staff_data['bio'],
                        'phone': staff_data['phone'],
                        'years_experience': staff_data['years_experience'],
                        'is_featured': staff_data['is_featured'],
                        'is_public': True,
                        'date_joined': date_joined,
                        'linkedin': staff_data.get('linkedin', ''),
                        'twitter': staff_data.get('twitter', ''),
                        'qualifications': '\n'.join(staff_data['qualifications']),
                        'specializations': '\n'.join(staff_data['specializations'])
                    }
                )
                
                # 🆕 NEW: Handle photo if specified
                if 'photo_path' in staff_data and staff_data['photo_path']:
                    # Try multiple possible paths for the photo
                    possible_paths = [
                        # Direct path from static root
                        os.path.join(settings.STATIC_ROOT or '', staff_data['photo_path']) if settings.STATIC_ROOT else None,
                        # Path from BASE_DIR/static
                        os.path.join(settings.BASE_DIR, 'static', staff_data['photo_path']),
                        # Path from current directory
                        os.path.join(settings.BASE_DIR, staff_data['photo_path']),
                        # Direct path (in case it's absolute)
                        staff_data['photo_path']
                    ]
                    
                    photo_loaded = False
                    for photo_path in possible_paths:
                        if photo_path and os.path.exists(photo_path):
                            try:
                                with open(photo_path, 'rb') as f:
                                    # Only update photo if staff doesn't have one or if it's different
                                    filename = os.path.basename(photo_path)
                                    if not staff.photo or staff.photo.name != f'staff/photos/{filename}':
                                        staff.photo.save(
                                            filename,
                                            File(f),
                                            save=True
                                        )
                                        self.stdout.write(f'  📸 Added photo for: {staff.user.get_full_name()}')
                                    else:
                                        self.stdout.write(f'  📸 Photo already exists for: {staff.user.get_full_name()}')
                                    photo_loaded = True
                                    break
                            except Exception as e:
                                self.stdout.write(f'  ⚠️  Error loading photo for {staff.user.get_full_name()}: {e}')
                    
                    if not photo_loaded:
                        self.stdout.write(f'  ⚠️  Photo not found for {staff.user.get_full_name()}: {staff_data["photo_path"]}')
                        # List the paths that were tried
                        self.stdout.write(f'      Tried paths:')
                        for path in possible_paths:
                            if path:
                                exists = "✅" if os.path.exists(path) else "❌"
                                self.stdout.write(f'        {exists} {path}')
                
                # 🔧 FIX: Update existing staff if data is different
                if not staff_created_flag:
                    # Check if staff data needs updating
                    staff_needs_update = False
                    
                    if staff.department != department:
                        staff.department = department
                        staff_needs_update = True
                    if staff.position != staff_data['position']:
                        staff.position = staff_data['position']
                        staff_needs_update = True
                    if staff.bio != staff_data['bio']:
                        staff.bio = staff_data['bio']
                        staff_needs_update = True
                    if staff.phone != staff_data['phone']:
                        staff.phone = staff_data['phone']
                        staff_needs_update = True
                    if staff.years_experience != staff_data['years_experience']:
                        staff.years_experience = staff_data['years_experience']
                        staff_needs_update = True
                    if staff.is_featured != staff_data['is_featured']:
                        staff.is_featured = staff_data['is_featured']
                        staff_needs_update = True
                    if staff.linkedin != staff_data.get('linkedin', ''):
                        staff.linkedin = staff_data.get('linkedin', '')
                        staff_needs_update = True
                    if staff.twitter != staff_data.get('twitter', ''):
                        staff.twitter = staff_data.get('twitter', '')
                        staff_needs_update = True
                    
                    # Check qualifications and specializations
                    new_qualifications = '\n'.join(staff_data['qualifications'])
                    new_specializations = '\n'.join(staff_data['specializations'])
                    if staff.qualifications != new_qualifications:
                        staff.qualifications = new_qualifications
                        staff_needs_update = True
                    if staff.specializations != new_specializations:
                        staff.specializations = new_specializations
                        staff_needs_update = True
                    
                    if staff_needs_update:
                        staff.save()
                        self.stdout.write(f'  🔄 Updated staff: {staff.user.get_full_name()} ({staff.employee_id})')
                    else:
                        self.stdout.write(f'  ℹ️  Staff already up-to-date: {staff.user.get_full_name()}')
                else:
                    self.stdout.write(f'  ✅ Created staff: {staff.user.get_full_name()} ({employee_id})')
                
                # Store staff for department head assignment
                full_name = f"{staff_data['first_name']} {staff_data['last_name']}"
                staff_created[full_name] = staff
                    
            except KeyError as e:
                self.stdout.write(f'  ❌ Missing key in staff data: {e}')
            except Exception as e:
                self.stdout.write(f'  ❌ Error creating staff {staff_data.get("first_name", "Unknown")}: {e}')
        
        # Now assign department heads
        self.stdout.write('👑 Assigning department heads...')
        for dept_data in DEPARTMENTS:
            if 'head_of_department' in dept_data:
                head_name = dept_data['head_of_department']
                if head_name in staff_created:
                    department = departments_created[dept_data['slug']]
                    department.head_of_department = staff_created[head_name]
                    department.save()
                    self.stdout.write(f'  ✅ Assigned {head_name} as head of {department.name}')
                else:
                    self.stdout.write(f'  ⚠️  Head not found: {head_name} for {dept_data["name"]}')
        
        self.stdout.write(f'📊 Total staff processed: {len(staff_created)}')



    def load_news_categories(self):
        """Load news categories using DRY approach"""
        self.stdout.write('📰 Loading news categories...')
        
        categories_data = [
            {'name': 'Tax Updates', 'slug': 'tax-updates', 'description': 'Latest updates on tax regulations, policies, and compliance requirements', 'color': '#007bff', 'icon': 'fas fa-calculator'},
            {'name': 'Business News', 'slug': 'business-news', 'description': 'Business developments, market insights, and industry trends', 'color': '#28a745', 'icon': 'fas fa-chart-line'},
            {'name': 'Regulatory Changes', 'slug': 'regulatory-changes', 'description': 'Updates on regulatory changes affecting businesses and individuals', 'color': '#dc3545', 'icon': 'fas fa-gavel'},
            {'name': 'Industry Insights', 'slug': 'industry-insights', 'description': 'Expert insights and analysis on accounting and finance industry', 'color': '#6f42c1', 'icon': 'fas fa-lightbulb'},
            {'name': 'Company News', 'slug': 'company-news', 'description': 'Updates and announcements from WJ Professionals', 'color': '#fd7e14', 'icon': 'fas fa-building'},
        ]
        
        created_count = updated_count = 0
        
        for cat_data in categories_data:
            cat_data['is_active'] = True
            
            obj, created = self.create_or_update_object(
                NewsCategory, 'slug', cat_data['slug'], cat_data,
                update_fields=['name', 'description', 'color', 'icon', 'is_active']
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        self.log_creation_stats('News Categories', created_count, updated_count)


    def load_news_articles(self):
        """Load news articles from centralized news_data.py"""
        self.stdout.write('📝 Loading news articles from centralized data...')
        
        # Import the centralized news data
        from apps.core.fixtures.news_data import NEWS_ARTICLES_DATA
        from django.contrib.auth.models import User
        from django.utils import timezone
        from datetime import timedelta
        import random
        
        # Create a default author if none exists
        author, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@wjprofessionals.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            author.set_password('admin123')
            author.save()
            self.stdout.write('  ✅ Created admin user (username: admin, password: admin123)')
        
        # Try to get staff members as potential authors
        try:
            from apps.staff.models import Staff
            staff_members = list(Staff.objects.filter(is_public=True))
            if staff_members:
                self.stdout.write(f'  📝 Found {len(staff_members)} staff members to use as authors')
        except:
            staff_members = []
            self.stdout.write('  ⚠️  Staff app not available, using admin as author')
        
        created_count = 0
        updated_count = 0
        
        for i, article_data in enumerate(NEWS_ARTICLES_DATA):
            try:
                # Determine category based on tags or article type
                category_mapping = {
                    'news': 'business-news',
                    'insight': 'industry-insights', 
                    'guide': 'tax-updates',
                    'update': 'regulatory-changes'
                }
                
                # Get category slug from article type or default to business-news
                category_slug = category_mapping.get(article_data.get('article_type', 'news'), 'business-news')
                
                # Try to get the category, create if doesn't exist
                try:
                    category = NewsCategory.objects.get(slug=category_slug)
                except NewsCategory.DoesNotExist:
                    # Create the category if it doesn't exist
                    category_names = {
                        'business-news': 'Business News',
                        'industry-insights': 'Industry Insights',
                        'tax-updates': 'Tax Updates', 
                        'regulatory-changes': 'Regulatory Changes'
                    }
                    category = NewsCategory.objects.create(
                        name=category_names.get(category_slug, 'General News'),
                        slug=category_slug,
                        color='#007bff'
                    )
                    self.stdout.write(f'  ✅ Created category: {category.name}')
                
                # Select author (prefer staff, fallback to admin)
                selected_author = author
                if staff_members:
                    # Rotate through staff members
                    staff_author = staff_members[i % len(staff_members)]
                    selected_author = staff_author.user
                
                # Generate realistic publish date (within last 6 months)
                days_ago = random.randint(1, 180)
                publish_date = timezone.now() - timedelta(days=days_ago)
                
                # Calculate read time based on content length
                content_words = len(article_data['content'].split())
                read_time = max(1, content_words // 200)  # Assume 200 words per minute
                
                # Prepare article data for model
                model_data = {
                    'title': article_data['title'],
                    'slug': article_data['slug'],
                    'excerpt': article_data['excerpt'],
                    'content': article_data['content'],
                    'author': selected_author,
                    'category': category,
                    'status': article_data.get('status', 'published'),
                    'is_featured': article_data.get('is_featured', False),
                    'is_breaking': article_data.get('is_breaking', False),
                    'tags': ', '.join(article_data.get('tags', [])),
                    'publish_date': publish_date,
                    'view_count': random.randint(10, 500),  # Random view count
                    'article_type': article_data.get('article_type', 'news')
                }
                
                # Create or update article
                article, created = NewsArticle.objects.get_or_create(
                    slug=article_data['slug'],
                    defaults=model_data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'  ✅ Created: {article.title}')
                    self.stdout.write(f'     📊 Category: {article.category.name}')
                    self.stdout.write(f'     👤 Author: {article.author.get_full_name()}')
                    self.stdout.write(f'     📅 Published: {article.publish_date.strftime("%Y-%m-%d")}')
                else:
                    # Update existing article if data has changed
                    updated_fields = []
                    for key, value in model_data.items():
                        if hasattr(article, key):
                            old_value = getattr(article, key)
                            # Skip author and category for updates to avoid conflicts
                            if key in ['author', 'category', 'publish_date']:
                                continue
                            if old_value != value:
                                setattr(article, key, value)
                                updated_fields.append(key)
                    
                    if updated_fields:
                        article.save()
                        updated_count += 1
                        self.stdout.write(f'  🔄 Updated: {article.title} ({", ".join(updated_fields)})')
                    else:
                        self.stdout.write(f'  ℹ️  Already up-to-date: {article.title}')
                        
            except Exception as e:
                self.stdout.write(f'  ❌ Error creating article {article_data.get("title", "Unknown")}: {e}')
        
        self.stdout.write(f'📊 News Articles - Created: {created_count}, Updated: {updated_count}')

    def load_testimonials(self):
        """Load testimonials from centralized news_data.py"""
        self.stdout.write('⭐ Loading testimonials from centralized data...')
        
        # Import the centralized testimonials data
        from apps.core.fixtures.news_data import TESTIMONIALS_DATA
        
        created_count = 0
        updated_count = 0
        
        for testimonial_data in TESTIMONIALS_DATA:
            # Map the data structure to match your Testimonial model
            testimonial_model_data = {
                'client_name': testimonial_data['client_name'],
                'company': testimonial_data['company'],
                'position': testimonial_data['position'],
                'testimonial': testimonial_data['content'],  # Map 'content' to 'testimonial'
                'rating': testimonial_data['rating'],
                'is_featured': testimonial_data['is_featured'],
                'is_approved': True,  # Auto-approve sample data
                'service_category': testimonial_data.get('service_category')
            }
            
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=testimonial_model_data['client_name'],
                company=testimonial_model_data['company'],
                defaults=testimonial_model_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  ✅ Created: {testimonial.client_name} ({testimonial.company})')
                self.stdout.write(f'     ⭐ Rating: {testimonial.rating}/5')
                self.stdout.write(f'     🏢 Service: {testimonial.service_category}')
            else:
                # Update existing testimonial if data has changed
                updated_fields = []
                for key, value in testimonial_model_data.items():
                    if hasattr(testimonial, key):
                        old_value = getattr(testimonial, key)
                        if old_value != value:
                            setattr(testimonial, key, value)
                            updated_fields.append(key)
                
                if updated_fields:
                    testimonial.save()
                    updated_count += 1
                    self.stdout.write(f'  🔄 Updated: {testimonial.client_name} ({", ".join(updated_fields)})')
                else:
                    self.stdout.write(f'  ℹ️  Already up-to-date: {testimonial.client_name}')
        
        self.stdout.write(f'📊 Testimonials - Created: {created_count}, Updated: {updated_count}')

    def load_faqs(self):
        """Load FAQs from centralized news_data.py"""
        self.stdout.write('❓ Loading FAQs from centralized data...')
        
        # Import the centralized FAQ data
        from apps.core.fixtures.news_data import FAQ_DATA
        
        created_count = 0
        updated_count = 0
        
        for faq_data in FAQ_DATA:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'category': faq_data['category'],
                    'is_featured': faq_data.get('is_featured', False),
                    'order': faq_data.get('order', 0)
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  ✅ Created: {faq.question[:50]}...')
                self.stdout.write(f'     📂 Category: {faq.category}')
            else:
                # Update existing FAQ if data has changed
                updated_fields = []
                if faq.answer != faq_data['answer']:
                    faq.answer = faq_data['answer']
                    updated_fields.append('answer')
                if faq.category != faq_data['category']:
                    faq.category = faq_data['category']
                    updated_fields.append('category')
                if faq.is_featured != faq_data.get('is_featured', False):
                    faq.is_featured = faq_data.get('is_featured', False)
                    updated_fields.append('is_featured')
                
                if updated_fields:
                    faq.save()
                    updated_count += 1
                    self.stdout.write(f'  🔄 Updated: {faq.question[:50]}... ({", ".join(updated_fields)})')
                else:
                    self.stdout.write(f'  ℹ️  Already up-to-date: {faq.question[:50]}...')
        
        self.stdout.write(f'📊 FAQs - Created: {created_count}, Updated: {updated_count}')

    def load_document_categories(self):
        """Load document categories"""
        self.stdout.write('📁 Loading document categories...')
        
        from apps.core.fixtures.document_data import DOCUMENT_CATEGORIES
        from apps.documents.models import DocumentCategory
        
        created_count = 0
        updated_count = 0

        for cat_data in DOCUMENT_CATEGORIES:
            category, created = DocumentCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'order': cat_data['order'],
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  ✅ Created: {category.name}')
            else:
                # Update existing category
                updated_fields = []
                if category.description != cat_data['description']:
                    category.description = cat_data['description']
                    updated_fields.append('description')
                if category.icon != cat_data['icon']:
                    category.icon = cat_data['icon']
                    updated_fields.append('icon')
                if category.color != cat_data['color']:
                    category.color = cat_data['color']
                    updated_fields.append('color')
                if category.order != cat_data['order']:
                    category.order = cat_data['order']
                    updated_fields.append('order')
                
                if updated_fields:
                    category.save()
                    updated_count += 1
                    self.stdout.write(f'  🔄 Updated: {category.name} ({", ".join(updated_fields)})')
                else:
                    self.stdout.write(f'  ℹ️  Already up-to-date: {category.name}')

        self.stdout.write(f'📊 Document Categories - Created: {created_count}, Updated: {updated_count}')

    def load_sample_documents(self):
        """Load sample documents (metadata only)"""
        self.stdout.write('📄 Loading sample documents...')
        
        from apps.core.fixtures.document_data import SAMPLE_DOCUMENTS
        from apps.documents.models import Document, DocumentCategory
        from django.contrib.auth.models import User
        
        # Get or create a system user for uploads
        system_user, created = User.objects.get_or_create(
            username='system',
            defaults={
                'email': 'system@wjprofessionals.com',
                'first_name': 'System',
                'last_name': 'User',
                'is_staff': True,
            }
        )
        
        if created:
            system_user.set_password('system123')
            system_user.save()
            self.stdout.write('  ✅ Created system user for document uploads')
        
        created_count = 0
        updated_count = 0
        
        for doc_data in SAMPLE_DOCUMENTS:
            try:
                category = DocumentCategory.objects.get(slug=doc_data['category_slug'])
                
                # Create document metadata
                document, created = Document.objects.get_or_create(
                    title=doc_data['title'],
                    defaults={
                        'description': doc_data['description'],
                        'category': category,
                        'access_level': doc_data['access_level'],
                        'file_type': doc_data['file_type'],
                        'tags': doc_data['tags'],
                        'is_featured': doc_data['is_featured'],
                        'meta_description': doc_data['meta_description'],
                        'uploaded_by': system_user,
                        'is_active': True,
                        'file_size': 1024,  # Dummy file size
                    }
                )
                
                if created:
                    # Create a dummy file for demonstration
                    dummy_content = f"Sample document: {doc_data['title']}\n\nThis is a placeholder document for demonstration purposes.\n\nContent: {doc_data['description']}"
                    filename = f"{slugify(doc_data['title'])}{doc_data['file_type']}"
                    
                    document.file.save(
                        filename,
                        ContentFile(dummy_content.encode()),
                        save=True
                    )
                    
                    created_count += 1
                    self.stdout.write(f'  ✅ Created: {document.title}')
                else:
                    # Update existing document if needed
                    updated_fields = []
                    if document.description != doc_data['description']:
                        document.description = doc_data['description']
                        updated_fields.append('description')
                    if document.category != category:
                        document.category = category
                        updated_fields.append('category')
                    if document.access_level != doc_data['access_level']:
                        document.access_level = doc_data['access_level']
                        updated_fields.append('access_level')
                    if document.is_featured != doc_data['is_featured']:
                        document.is_featured = doc_data['is_featured']
                        updated_fields.append('is_featured')
                    
                    if updated_fields:
                        document.save()
                        updated_count += 1
                        self.stdout.write(f'  🔄 Updated: {document.title} ({", ".join(updated_fields)})')
                    else:
                        self.stdout.write(f'  ℹ️  Already up-to-date: {document.title}')
                    
            except DocumentCategory.DoesNotExist:
                self.stdout.write(f'  ❌ Category not found: {doc_data["category_slug"]}')
            except Exception as e:
                self.stdout.write(f'  ❌ Error creating document {doc_data["title"]}: {e}')
        
        self.stdout.write(f'📊 Sample Documents - Created: {created_count}, Updated: {updated_count}')
        if created_count > 0:
            self.stdout.write(
                self.style.WARNING('⚠️  Note: Sample documents contain dummy files. Replace with real documents as needed.')
            )

# Update your existing handle method
def handle(self, *args, **options):
    if options['clear']:
        self.stdout.write('Clearing existing data...')
        self.clear_data()

    self.stdout.write('Loading sample data...')
    
    # Load data in order
    self.load_company_data()
    self.load_service_categories()
    self.load_services()
    self.load_staff()
    self.load_news_categories()
    self.load_news_articles()
    self.load_testimonials()
    self.load_faqs()
    
    # ADD THESE TWO LINES:
    self.load_document_categories()
    self.load_sample_documents()
    
    self.stdout.write(
        self.style.SUCCESS('Successfully loaded sample data!')
    )
    # Add document counts
    try:
        from apps.documents.models import DocumentCategory, Document
        self.stdout.write(f'   • Document Categories: {DocumentCategory.objects.count()}')
        self.stdout.write(f'   • Documents: {Document.objects.count()}')
    except ImportError:
        self.stdout.write('   • Documents app not available')

# Update your clear_data method to include documents
def clear_data(self):
    """Clear existing data"""
    self.stdout.write('Clearing existing data...')
    
    # Clear documents first (if available)
    try:
        from apps.documents.models import Document, DocumentCategory
        Document.objects.all().delete()
        self.stdout.write('Cleared Document data')
        DocumentCategory.objects.all().delete()
        self.stdout.write('Cleared DocumentCategory data')
    except ImportError:
        self.stdout.write('Documents app not available for clearing')
    
    # Clear in reverse dependency order (your existing code)
    FAQ.objects.all().delete()
    self.stdout.write('Cleared FAQ data')
    
    Testimonial.objects.all().delete()
    self.stdout.write('Cleared Testimonial data')
    
    NewsArticle.objects.all().delete()
    self.stdout.write('Cleared NewsArticle data')
    
    NewsCategory.objects.all().delete()
    self.stdout.write('Cleared NewsCategory data')
    
    Staff.objects.all().delete()
    self.stdout.write('Cleared Staff data')
    
    Department.objects.all().delete()
    self.stdout.write('Cleared Department data')
    
    Service.objects.all().delete()
    self.stdout.write('Cleared Service data')
    
    ServiceCategory.objects.all().delete()
    self.stdout.write('Cleared ServiceCategory data')
    
    Company.objects.all().delete()
    self.stdout.write('Cleared Company data')