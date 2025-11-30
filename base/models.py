from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(default='avatar.svg', null=True)

class Task(models.Model):
    priorities = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    ]
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True, default='No Description')
    priority = models.CharField(max_length=30, blank=True, null=True, default='', choices=priorities )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    deadline = models.DateField(blank=True, null=True)
    created = models.TimeField(auto_now_add=True)
    updated = models.TimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.name

