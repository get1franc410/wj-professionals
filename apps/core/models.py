# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\core\models.py
"""
Core Models
===========
Core models for the WJ Professionals website
"""

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import RegexValidator
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
from django.db.models import Avg, Count 

class Company(models.Model):
    """Company information model"""
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    description = CKEditor5Field('Description', config_name='default', blank=True)
    mission = CKEditor5Field('Mission', config_name='default', blank=True)
    vision = CKEditor5Field('Vision', config_name='default', blank=True)
    values = CKEditor5Field('Values', config_name='default', blank=True)
    about_us = CKEditor5Field('About Us', config_name='default', blank=True)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Nigeria')

    working_hours = models.TextField(blank=True)
    certifications = models.JSONField(default=list, blank=True)
    
    # Stats (these will be overridden by properties)
    clients_served = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    
    # Online Presence
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    
    
    # Business Details
    established_year = models.PositiveIntegerField(null=True, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Media
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Companies"
    
    def __str__(self):
        return self.name
    
    @property
    def years_of_experience(self):
        """Calculate years of experience from establishment year"""
        if self.established_year:
            current_year = timezone.now().year
            return current_year - self.established_year
        return 0
    @property
    def years_experience(self):
        """Alias for years_of_experience"""
        return self.years_of_experience
    
    @property
    def founded_year(self):
        """Alias for established_year for backward compatibility"""
        return self.established_year
    
    @property
    def review_stats(self):
        """Get review statistics from the reviews app"""
        try:
            from apps.reviews.models import Review
            return Review.objects.filter(status='approved').aggregate(
                avg_rating=Avg('rating'),
                total_reviews=Count('id'),
                five_star=Count('id', filter=models.Q(rating=5)),
                four_star=Count('id', filter=models.Q(rating=4)),
                three_star=Count('id', filter=models.Q(rating=3)),
                two_star=Count('id', filter=models.Q(rating=2)),
                one_star=Count('id', filter=models.Q(rating=1)),
            )
        except ImportError:
            return {
                'avg_rating': 4.7,
                'total_reviews': 0,
                'five_star': 0,
                'four_star': 0,
                'three_star': 0,
                'two_star': 0,
                'one_star': 0,
            }
    
    @property
    def overall_rating(self):
        """Get overall rating from reviews"""
        stats = self.review_stats
        return round(stats['avg_rating'] or 4.7, 1)
    
    @property
    def total_reviews(self):
        """Get total number of reviews"""
        stats = self.review_stats
        return stats['total_reviews'] or 0
    
    @property
    def featured_reviews(self):
        """Get featured reviews"""
        try:
            from apps.reviews.models import Review
            return Review.objects.filter(
                status='approved',
                is_featured=True
            ).order_by('-created_at')[:6]
        except ImportError:
            return []
    
    # ✅ ADDED: Singleton pattern method
    @classmethod
    def get_instance(cls):
        """Get the company instance (singleton pattern)"""
        company = cls.objects.first()
        if not company:
            # Create default company if none exists
            company = cls.objects.create(
                name='WJ Professionals',
                tagline='Your Trusted Accounting Partner in Nigeria',
                email='info@wjprofessionals.com',
                phone='+234-803-065-5969',
                address='Plot 123, Ademola Adetokunbo Crescent, Wuse II, Abuja',
                city='Abuja',
                state='FCT',
                postal_code='900001',
                established_year=2010,
                clients_served=500,
                projects_completed=1200,
            )
        return company


class ServiceCategory(models.Model):
    """Service category model"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="fas fa-cog")
    color = models.CharField(max_length=7, default="#007bff")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Service Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:services_category', kwargs={'slug': self.slug})


class Service(models.Model):
    """Service model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    
    short_description = models.TextField(max_length=300)
    description = CKEditor5Field('Description', config_name='default')
    
    # Pricing
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_type = models.CharField(max_length=20, choices=[
        ('fixed', 'Fixed Price'),
        ('hourly', 'Hourly Rate'),
        ('project', 'Project Based'),
        ('consultation', 'Consultation Required'),
    ], default='consultation')
    
    # Features and Benefits
    features = models.TextField(help_text="One feature per line")
    benefits = models.TextField(blank=True, help_text="One benefit per line")
    delivery_time = models.CharField(max_length=100, blank=True, help_text="Expected delivery timeframe")
        
    # Media
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.short_description[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:service_detail', kwargs={'slug': self.slug})

    @property
    def feature_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    @property
    def benefit_list(self):
        return [b.strip() for b in self.benefits.split('\n') if b.strip()]


class Position(models.Model):
    """Position/Job title model"""
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=[
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive'),
    ], default='mid')
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    """Client testimonial model"""
    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    
    testimonial = models.TextField()
    service_category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='testimonials',
        help_text="Service category this testimonial relates to"
    )
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    
    # Media
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    
    # Status
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Testimonial by {self.client_name}"


class FAQ(models.Model):
    """Frequently Asked Questions model"""
    question = models.CharField(max_length=300)
    answer = CKEditor5Field('Answer', config_name='default')
    category = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.question


class ContactSubmission(models.Model):
    """Contact form submission model"""
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('tax', 'Tax Services'),
        ('business', 'Business Advisory'),
        ('accounting', 'Accounting Services'),
        ('audit', 'Audit Services'),
        ('consultation', 'Free Consultation'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False, help_text="Mark as read when reviewed")
    
    # Status
    is_read = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"
