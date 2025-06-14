# Generated by Django 4.2.11 on 2025-05-30 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_company_about_us_company_certifications_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='is_active',
        ),
        migrations.AddField(
            model_name='staff',
            name='is_public',
            field=models.BooleanField(default=True, help_text='Show on public website'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='Show on homepage'),
        ),
    ]
