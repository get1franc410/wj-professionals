from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Client Information
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_company = models.CharField(max_length=100, blank=True, null=True)
    client_position = models.CharField(max_length=100, blank=True, null=True)
    
    # Review Content
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200, help_text="Brief title for your review")
    review_text = models.TextField(help_text="Share your experience with our services")
    
    # Service Information
    service_used = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Which service did you use?"
    )
    
    # Moderation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Client Review'
        verbose_name_plural = 'Client Reviews'
    
    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"
    
    def get_absolute_url(self):
        return reverse('reviews:review_detail', kwargs={'pk': self.pk})
    
    def approve(self):
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.save()
    
    @property
    def star_range(self):
        return range(1, 6)
    
    @property
    def filled_stars(self):
        return range(1, self.rating + 1)
    
    @property
    def empty_stars(self):
        return range(self.rating + 1, 6)

class ReviewResponse(models.Model):
    """Admin responses to reviews"""
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='response')
    response_text = models.TextField()
    responder_name = models.CharField(max_length=100, default="WJ Professionals Team")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.review.client_name}"
