# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\news\models.py
"""
News Models
===========
Models for news and blog functionality
"""

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class NewsCategory(models.Model):
    """News category model"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#007bff", help_text='Hex color code')
    icon = models.CharField(max_length=50, default="fas fa-newspaper")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "News Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:category', kwargs={'slug': self.slug})

    @property
    def article_count(self):
        return self.articles.filter(status='published').count()


class NewsArticle(models.Model):
    """News article model"""
    
    ARTICLE_TYPES = [
        ('news', 'News'),
        ('update', 'Company Update'),
        ('announcement', 'Announcement'),
        ('insight', 'Industry Insight'),
        ('guide', 'Tax Guide'),
        ('regulation', 'Regulatory Update'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPES, default='news')
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='articles')
    
    # Content
    excerpt = models.TextField(max_length=300, help_text="Brief summary for previews")
    content = CKEditor5Field('Content', config_name='extends')
    
    # Media
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    image_caption = models.CharField(max_length=200, blank=True)
    
    # Author Information
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    co_authors = models.ManyToManyField(User, related_name='co_authored_articles', blank=True)
    
    # Publication Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    publish_date = models.DateTimeField(default=timezone.now, help_text="When this article should be published")
    published_at = models.DateTimeField(blank=True, null=True, help_text="Automatically set when status changes to published")
    
    # Engagement
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    
    # SEO fields - ADDED meta_title
    meta_title = models.CharField(max_length=60, blank=True, help_text='SEO title')
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.TextField(blank=True)
    
    # Settings
    is_featured = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    
    # Tags - Changed from JSONField to CharField for compatibility
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publish_date', '-created_at'] 
        indexes = [
            models.Index(fields=['status', 'publish_date']), 
            models.Index(fields=['category', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-generate meta fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        
        # Set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        elif self.status != 'published':
            self.published_at = None
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug})
    
    def get_read_time(self):
        """Calculate estimated reading time"""
        if self.content:
            word_count = len(self.content.split())
            return max(1, round(word_count / 200))  # 200 words per minute
        return 1
    
    @property
    def read_time(self):
        return self.get_read_time()
    
    @property
    def is_published(self):
        return self.status == 'published' and self.published_at

    @property
    def tag_list(self):
        """Return tags as a list"""
        if isinstance(self.tags, str):
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return self.tags if isinstance(self.tags, list) else []

    def get_related_articles(self, limit=3):
        """Get related articles based on category and tags"""
        related = NewsArticle.objects.filter(
            category=self.category,
            status='published',
            publish_date__lte=timezone.now()
        ).exclude(id=self.id)
        
        return related[:limit]


class NewsletterSubscriber(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)  # Added for compatibility
    
    # Preferences
    categories = models.ManyToManyField(NewsCategory, blank=True)
    frequency = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], default='weekly')
    
    # Status
    is_active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, blank=True)
    
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    last_email_sent = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email

    def unsubscribe(self):
        """Unsubscribe user"""
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()


class Comment(models.Model):
    """Article comment model"""
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    
    is_approved = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author_name} on {self.article.title}"


class ArticleView(models.Model):
    """Track article views"""
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['article', 'ip_address']
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.article.title} - {self.ip_address}"
