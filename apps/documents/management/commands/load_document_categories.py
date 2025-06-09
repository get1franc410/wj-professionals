from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.documents.models import DocumentCategory

class Command(BaseCommand):
    help = 'Load document categories with sample data'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Loading document categories...')
        )

        categories_data = [
            {
                'name': 'Tax Forms & Guides',
                'description': 'Essential tax forms, guides, and compliance documents for individuals and businesses.',
                'icon': 'fas fa-file-invoice-dollar',
                'color': '#28a745',
                'order': 1,
            },
            {
                'name': 'Business Formation',
                'description': 'Documents and templates for starting and structuring your business.',
                'icon': 'fas fa-building',
                'color': '#007bff',
                'order': 2,
            },
            {
                'name': 'Financial Planning',
                'description': 'Tools and templates for budgeting, forecasting, and financial analysis.',
                'icon': 'fas fa-chart-line',
                'color': '#17a2b8',
                'order': 3,
            },
            {
                'name': 'Compliance & Legal',
                'description': 'Regulatory compliance documents and legal templates.',
                'icon': 'fas fa-balance-scale',
                'color': '#6f42c1',
                'order': 4,
            },
            {
                'name': 'Accounting Templates',
                'description': 'Ready-to-use accounting templates and spreadsheets.',
                'icon': 'fas fa-calculator',
                'color': '#fd7e14',
                'order': 5,
            },
            {
                'name': 'Client Resources',
                'description': 'Helpful resources and guides for our clients.',
                'icon': 'fas fa-users',
                'color': '#20c997',
                'order': 6,
            },
            {
                'name': 'Software Guides',
                'description': 'Tutorials and guides for accounting software and tools.',
                'icon': 'fas fa-laptop',
                'color': '#e83e8c',
                'order': 7,
            },
            {
                'name': 'Industry Reports',
                'description': 'Market analysis and industry-specific reports.',
                'icon': 'fas fa-chart-bar',
                'color': '#6610f2',
                'order': 8,
            },
        ]

        created_count = 0
        updated_count = 0

        for cat_data in categories_data:
            slug = slugify(cat_data['name'])
            
            category, created = DocumentCategory.objects.get_or_create(
                slug=slug,
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
                category.description = cat_data['description']
                category.icon = cat_data['icon']
                category.color = cat_data['color']
                category.order = cat_data['order']
                category.save()
                updated_count += 1
                self.stdout.write(f'  🔄 Updated: {category.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Completed! Created: {created_count}, Updated: {updated_count}'
            )
        )
