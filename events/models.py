from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission

class Event(models.Model):

    class Meta:
        app_label = 'events'
        
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    categories = models.CharField(max_length=255)

    registrations = models.ManyToManyField(User, through='Registration', related_name='registered_events')

    def __str__(self):
        return self.title
    

class Registration(models.Model):
    EVENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=EVENT_STATUS_CHOICES, default='pending')

    # Add any other fields or methods you need for the Registration model

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Venue(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    amenities = models.TextField()
    availability = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def get_upcoming_events(self):
        return self.event_set.filter(date__gte=timezone.now())
    
class User(AbstractUser):
    # Add any additional fields or relationships you need
    registration_history = models.ManyToManyField(Event, through='Registration', related_name='registered_users')
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_set')

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

