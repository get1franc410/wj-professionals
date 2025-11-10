# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web_updated_temp\wj_professionals\apps\core\management\commands\sync_company_data.py
from django.core.management.base import BaseCommand
from apps.core.models import Company
from apps.core.fixtures.company_data import COMPANY_DATA

class Command(BaseCommand):
    help = 'Sync company data from fixtures to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update even if database has newer data',
        )

    def handle(self, *args, **options):
        self.stdout.write('🔄 Syncing company data from fixtures to database...')
        
        # Get or create company
        company, created = Company.objects.get_or_create(
            name=COMPANY_DATA['name'],
            defaults=COMPANY_DATA
        )
        
        if created:
            self.stdout.write(f'✅ Created new company: {company.name}')
        else:
            if options['force']:
                # Update all fields from fixtures
                for key, value in COMPANY_DATA.items():
                    if hasattr(company, key):
                        setattr(company, key, value)
                company.save()
                self.stdout.write(f'🔄 Force updated company: {company.name}')
            else:
                self.stdout.write(f'ℹ️  Company already exists: {company.name}')
                self.stdout.write('   Use --force to update from fixtures')
        
        # Display current stats
        self.stdout.write(f'📊 Current Company Stats:')
        self.stdout.write(f'   • Name: {company.name}')
        self.stdout.write(f'   • Email: {company.email}')
        self.stdout.write(f'   • Phone: {company.phone}')
        self.stdout.write(f'   • Clients: {company.clients_served}')
        self.stdout.write(f'   • Projects: {company.projects_completed}')
        self.stdout.write(f'   • Years Experience: {company.years_of_experience}')
