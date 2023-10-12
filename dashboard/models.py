from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 

# Create your models here.

class User(AbstractUser):
    pass

class Activity(models.Model):
    PROFESSIONAL = 'professional'
    PERSONAL = 'personal'
    DEVELOPMENT = 'development'
    MINISTRY= 'ministry'
    HEALTH= 'health'
    CATEGORY_CHOICES = [
        (PROFESSIONAL, 'Professional'),
        (PERSONAL, 'Personal'),
        (DEVELOPMENT, 'Development'),
        (MINISTRY, 'Ministry'),
        (HEALTH, 'Ministry')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    linked_goals = models.ManyToManyField('Goal', related_name='linked_activities')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Link activities to goals using a ManyToManyField

    def __str__(self):
        return self.title

class Goal(models.Model):
    CATEGORY_CHOICES = [
        ('professional', 'Professional'),
        ('personal', 'Personal'),
        ('development', 'Development'),
        ('spiritual', 'Spiritual'),
        ('faith', 'Faith'),
        ('charity', 'Charity'),
    ]

    TYPE_CHOICES = [
        ('long_term', 'Long Term'),
        ('mid_term', 'Mid Term'),
        ('weekly', 'Weekly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    summary = models.TextField()
    description = models.TextField()
    action_items = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title