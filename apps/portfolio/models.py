# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\portfolio\models.py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Industry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="fas fa-industry")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Industries"
    
    def __str__(self):
        return self.name

class Client(models.Model):
    CLIENT_TYPES = [
        ('individual', 'Individual'),
        ('sme', 'Small & Medium Enterprise'),
        ('corporate', 'Large Corporation'),
        ('ngo', 'Non-Governmental Organization'),
        ('government', 'Government Agency'),
    ]
    
    PROJECT_STATUS = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPES)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    
    # Contact Information
    contact_person = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    
    # Visual Elements
    logo = models.ImageField(upload_to='clients/', blank=True)
    banner_image = models.ImageField(upload_to='clients/banners/', blank=True)
    
    # Project Details
    project_title = models.CharField(max_length=300)
    project_description = CKEditor5Field('Project Description', config_name='default')
    services_provided = models.JSONField(default=list, help_text="List of services provided")
    project_duration = models.CharField(max_length=100)
    project_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    project_status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='completed')
    
    # Timeline
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    # Results & Outcomes
    key_achievements = models.JSONField(default=list, help_text="List of key achievements")
    challenges_overcome = CKEditor5Field('Challenges Overcome', config_name='default', blank=True)
    client_benefits = CKEditor5Field('Client Benefits', config_name='default', blank=True) 
    
    # Testimonial
    testimonial = CKEditor5Field('Testimonial', config_name='default', blank=True)
    testimonial_author = models.CharField(max_length=200, blank=True)
    testimonial_position = models.CharField(max_length=200, blank=True)
    
    # Display Settings
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    # SEO
    meta_description = models.TextField(max_length=160, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.project_title}"

class ProjectImage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='projects/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.client.name} - Image {self.order}"

class CaseStudy(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='case_study')
    
    # Problem Statement
    problem_statement = CKEditor5Field('Problem Statement', config_name='default')  
    client_situation = CKEditor5Field('Client Situation', config_name='default') 
    
    # Solution
    our_approach = CKEditor5Field('Our Approach', config_name='default') 
    methodology = CKEditor5Field('Methodology', config_name='default')
    tools_used = models.JSONField(default=list)
    
    # Results
    quantitative_results = models.JSONField(default=list, help_text="Measurable outcomes")
    qualitative_results = CKEditor5Field('Qualitative Results', config_name='default')
    roi_achieved = models.CharField(max_length=100, blank=True)
    
    # Lessons Learned
    lessons_learned = CKEditor5Field('Lessons Learned', config_name='default', blank=True)  
    future_recommendations = CKEditor5Field('Future Recommendations', config_name='default', blank=True)
    
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Case Study: {self.client.name}"
