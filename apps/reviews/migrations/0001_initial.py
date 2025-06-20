# Generated by Django 4.2.11 on 2025-06-01 10:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100)),
                ('client_email', models.EmailField(max_length=254)),
                ('client_company', models.CharField(blank=True, max_length=100, null=True)),
                ('client_position', models.CharField(blank=True, max_length=100, null=True)),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('title', models.CharField(help_text='Brief title for your review', max_length=200)),
                ('review_text', models.TextField(help_text='Share your experience with our services')),
                ('service_used', models.CharField(blank=True, help_text='Which service did you use?', max_length=100, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('is_featured', models.BooleanField(default=False, help_text='Show on homepage')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Client Review',
                'verbose_name_plural': 'Client Reviews',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReviewResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField()),
                ('responder_name', models.CharField(default='WJ Professionals Team', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('review', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='reviews.review')),
            ],
        ),
    ]
