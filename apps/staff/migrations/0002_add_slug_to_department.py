# apps/staff/migrations/0002_add_slug_to_department.py

from django.db import migrations, models
from django.utils.text import slugify

def populate_department_slugs(apps, schema_editor):
    """Populate slug field for existing departments"""
    Department = apps.get_model('staff', 'Department')
    
    for dept in Department.objects.all():
        if not dept.slug:
            base_slug = slugify(dept.name)
            slug = base_slug
            counter = 1
            
            # Ensure unique slug
            while Department.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            dept.slug = slug
            dept.save()

def reverse_populate_department_slugs(apps, schema_editor):
    """Reverse migration - clear slug field"""
    Department = apps.get_model('staff', 'Department')
    Department.objects.update(slug='')

class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        # First add the field without unique constraint
        migrations.AddField(
            model_name='department',
            name='slug',
            field=models.SlugField(blank=True, unique=False),  # Not unique yet
        ),
        
        # Populate the slug field
        migrations.RunPython(
            populate_department_slugs,
            reverse_populate_department_slugs,
        ),
        
        # Now make it unique
        migrations.AlterField(
            model_name='department',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
