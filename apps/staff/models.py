# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\staff\models.py
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field 
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Department(models.Model):
    """Company departments"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    head_of_department = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='department_head')
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def active_staff_count(self):
        return self.staff.filter(is_active=True, is_public=True).count()

class Staff(models.Model):
    POSITION_CHOICES = [
        ('managing_partner', 'Managing Partner'),
        ('senior_partner', 'Senior Partner'),
        ('partner', 'Partner'),
        ('senior_manager', 'Senior Manager'),
        ('manager', 'Manager'),
        ('senior_associate', 'Senior Associate'),
        ('associate', 'Associate'),
        ('junior_associate', 'Junior Associate'),
        ('admin', 'Administrative Staff'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    photo = models.ImageField(upload_to='staff/photos/', null=True, blank=True)
    
    # Personal Information
    bio = CKEditor5Field('Biography', config_name='default', blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Professional Information
    qualifications = models.JSONField(default=list, help_text="List of professional qualifications")
    certifications = models.JSONField(default=list, help_text="List of certifications")
    specializations = models.JSONField(default=list, help_text="Areas of specialization")
    years_experience = models.PositiveIntegerField(default=0)
    
    # Contact Information
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    # Employment Details
    date_joined = models.DateTimeField(default=timezone.now)
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Display Settings
    is_public = models.BooleanField(default=True, help_text="Show on public website")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'position', 'user__first_name']
        verbose_name_plural = "Staff"
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_full_name(self):
        """Get the full name of the staff member"""
        return f"{self.user.first_name} {self.user.last_name}".strip()
    
    def get_absolute_url(self):
        return reverse('staff:staff_detail', kwargs={'pk': self.pk})
    
    def get_photo_url(self):
        """Get photo URL - check both media and static locations"""
        if self.photo and hasattr(self.photo, 'url'):
            try:
                # Try to access the file to see if it exists
                _ = self.photo.url
                return self.photo.url
            except:
                pass
        
        # Fallback to static images based on naming convention
        if hasattr(self, 'user') and self.user:
            # Try CEO photo first
            if self.position == 'managing_partner':
                return '/static/images/ceo_portrait.jpg'
            
            # Try numbered staff photos
            staff_id = getattr(self, 'id', 0)
            if staff_id and staff_id <= 8:  # We have staff_2.jpg to staff_8.jpg
                return f'/static/images/staff_{staff_id + 1}.jpg'
        
        # Default placeholder
        return '/static/images/placeholder-avatar.jpg'

    @property
    def photo_url(self):
        """Property for easy template access"""
        return self.get_photo_url()
    
    @property
    def full_name(self):
        return self.user.get_full_name()

class Achievement(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_achieved = models.DateField()
    certificate = models.FileField(upload_to='achievements/', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_achieved']
    
    def __str__(self):
        return f"{self.staff.full_name} - {self.title}"

# class PerformanceReview(models.Model):
#     """Staff performance reviews"""
    
#     REVIEW_PERIODS = [
#         ('quarterly', 'Quarterly'),
#         ('semi_annual', 'Semi-Annual'),
#         ('annual', 'Annual'),
#         ('probation', 'Probation Review'),
#         ('project', 'Project Review'),
#     ]
    
#     RATINGS = [
#         (1, 'Poor'),
#         (2, 'Below Average'),
#         (3, 'Average'),
#         (4, 'Good'),
#         (5, 'Excellent'),
#     ]
    
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='reviews')
#     reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='conducted_reviews')
    
#     review_period = models.CharField(max_length=20, choices=REVIEW_PERIODS)
#     review_date = models.DateField()
#     period_start = models.DateField()
#     period_end = models.DateField()
    
#     # Ratings
#     overall_rating = models.PositiveIntegerField(
#         choices=RATINGS,
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
#     technical_skills = models.PositiveIntegerField(
#         choices=RATINGS,
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
#     communication = models.PositiveIntegerField(
#         choices=RATINGS,
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
#     teamwork = models.PositiveIntegerField(
#         choices=RATINGS,
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
#     punctuality = models.PositiveIntegerField(
#         choices=RATINGS,
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
    
#     # Comments
#     achievements = CKEditor5Field('Achievements', config_name='default', blank=True)  # Fixed
#     areas_for_improvement = CKEditor5Field('Areas for Improvement', config_name='default', blank=True)  # Fixed
#     goals_next_period = CKEditor5Field('Goals for Next Period', config_name='default', blank=True)  # Fixed
#     reviewer_comments = CKEditor5Field('Reviewer Comments', config_name='default', blank=True)  # Fixed
#     staff_comments = CKEditor5Field('Staff Comments', config_name='default', blank=True)  # Fixed
    
#     # Status
#     is_finalized = models.BooleanField(default=False)
#     staff_acknowledged = models.BooleanField(default=False)
#     acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-review_date']
#         unique_together = ['staff', 'review_period', 'period_start', 'period_end']
    
#     def __str__(self):
#         return f"{self.staff.full_name} - {self.get_review_period_display()} {self.review_date.year}"


# class LeaveRequest(models.Model):
#     """Staff leave requests"""
    
#     LEAVE_TYPES = [
#         ('annual', 'Annual Leave'),
#         ('sick', 'Sick Leave'),
#         ('maternity', 'Maternity Leave'),
#         ('paternity', 'Paternity Leave'),
#         ('emergency', 'Emergency Leave'),
#         ('study', 'Study Leave'),
#         ('unpaid', 'Unpaid Leave'),
#     ]
    
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#         ('cancelled', 'Cancelled'),
#     ]
    
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='leave_requests')
#     leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    
#     start_date = models.DateField()
#     end_date = models.DateField()
#     days_requested = models.PositiveIntegerField()
    
#     reason = models.TextField()
#     supporting_document = models.FileField(upload_to='staff/leave_docs/', blank=True)
    
#     # Approval
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
#     approval_date = models.DateTimeField(null=True, blank=True)
#     approval_comments = models.TextField(blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-created_at']
    
#     def __str__(self):
#         return f"{self.staff.full_name} - {self.get_leave_type_display()} ({self.start_date} to {self.end_date})"