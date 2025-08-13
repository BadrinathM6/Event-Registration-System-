from django import forms
from django.utils import timezone
from .models import Event, Registration

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'capacity']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if date <= timezone.now():
            raise forms.ValidationError('Event date must be in the future.')
        return date
    
    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        if capacity < 1:
            raise forms.ValidationError('Capacity must be at least 1.')
        return capacity

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['attendee_name', 'attendee_email', 'phone_number']
        widgets = {
            'attendee_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'attendee_email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number (Optional)'}),
        }

class EventFilterForm(forms.Form):
    SORT_CHOICES = [
        ('date', 'Date (Ascending)'),
        ('-date', 'Date (Descending)'),
        ('title', 'Title (A-Z)'),
        ('-title', 'Title (Z-A)'),
        ('capacity', 'Capacity (Low to High)'),
        ('-capacity', 'Capacity (High to Low)'),
    ]
    
    STATUS_CHOICES = [
        ('', 'All Events'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search events...'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial='date')
