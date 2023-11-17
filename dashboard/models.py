from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 

# Create your models here.

CATEGORY_CHOICES = [
    ('faith', 'Faith'),
    ('financial', 'Financial'),
    ('personal', 'Personal'),
    ('development', 'Development'),
    ('professional', 'Professional'),
]

TYPE_CHOICES = [
        ('long_term', 'Long Term (5-20 years)'),
        ('mid_term', 'Mid Term (1-5 years)'),
        ('short_term', 'Short Term (< 12 Months)'),
    ]

STATUS_CHOICES = [
    ('Not Started', 'Not Started'),
    ('In Progress', 'In Progress'),
    ('Achieved', 'Achieved'),
]

class User(AbstractUser):
    pass

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    linked_goal = models.ForeignKey('Goal', on_delete=models.SET_NULL, null=True, blank=True)

    def category(self):
        # Retrieve the category from the linked goal
        if self.linked_goal.exists():
            return self.linked_goal.first().category
        return ""

    def __str__(self):
        return self.title

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    actions = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    target_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    achieved_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title