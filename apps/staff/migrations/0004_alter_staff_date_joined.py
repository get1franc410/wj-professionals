# Generated by Django 4.2.11 on 2025-05-28 15:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_staff_email_alter_staff_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
