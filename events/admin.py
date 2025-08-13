from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'capacity', 'registered_count', 'status']
    list_filter = ['status', 'date']
    search_fields = ['title', 'location']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['attendee_name', 'attendee_email', 'event', 'status', 'registered_at']
    list_filter = ['status', 'registered_at', 'event']
    search_fields = ['attendee_name', 'attendee_email', 'event__title']
