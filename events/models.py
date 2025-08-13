from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Event(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        if self.date and self.date <= timezone.now():
            raise ValidationError('Event date must be in the future.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def registered_count(self):
        return self.registrations.filter(status='confirmed').count()
    
    @property
    def available_spots(self):
        return self.capacity - self.registered_count
    
    @property
    def is_full(self):
        return self.registered_count >= self.capacity
    
    @property
    def can_register(self):
        return (self.status == 'active' and 
                not self.is_full and 
                self.date > timezone.now())

class Registration(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('waitlist', 'Waitlist'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.EmailField(validators=[EmailValidator()])
    phone_number = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'attendee_email']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.attendee_name} - {self.event.title}"
    
    def clean(self):
        # Only validate if event is set (to avoid RelatedObjectDoesNotExist error)
        if hasattr(self, 'event') and self.event:
            if self.event.status == 'cancelled':
                raise ValidationError('Cannot register for a cancelled event.')
            
            if self.event.date <= timezone.now():
                raise ValidationError('Cannot register for past events.')
    
    def save(self, *args, **kwargs):
        if not self.pk:  # New registration
            # Only call clean if event is set
            if hasattr(self, 'event') and self.event:
                self.clean()
                if self.event.is_full:
                    self.status = 'waitlist'
        super().save(*args, **kwargs)