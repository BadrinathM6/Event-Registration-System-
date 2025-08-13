from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Event, Registration
from .forms import EventForm, RegistrationForm, EventFilterForm

def event_list(request):
    events = Event.objects.all()
    form = EventFilterForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        status = form.cleaned_data.get('status')
        sort_by = form.cleaned_data.get('sort_by')
        
        if search:
            events = events.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        
        if status:
            events = events.filter(status=status)
        
        if sort_by:
            events = events.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(events, 6)  # 6 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'events': page_obj,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registrations = event.registrations.filter(status='confirmed')
    
    context = {
        'event': event,
        'registrations': registrations,
        'can_register': event.can_register,
    }
    return render(request, 'events/event_detail.html', context)

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})

def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if not event.can_register:
        messages.error(request, 'Registration is not available for this event.')
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Check if already registered
                email = form.cleaned_data.get('attendee_email')
                
                existing_registration = Registration.objects.filter(
                    event=event,
                    attendee_email=email
                ).first()
                
                if existing_registration:
                    messages.error(request, 'You are already registered for this event.')
                    return redirect('event_detail', pk=pk)
                
                # Additional validations before saving
                if event.status == 'cancelled':
                    messages.error(request, 'Cannot register for a cancelled event.')
                    return redirect('event_detail', pk=pk)
                
                if event.date <= timezone.now():
                    messages.error(request, 'Cannot register for past events.')
                    return redirect('event_detail', pk=pk)
                
                # Create new registration
                registration = form.save(commit=False)
                registration.event = event
                
                # Check if event is full and set status accordingly
                if event.is_full:
                    registration.status = 'waitlist'
                else:
                    registration.status = 'confirmed'
                
                registration.save()
                
                if registration.status == 'waitlist':
                    messages.warning(request, 'Event is full. You have been added to the waitlist.')
                else:
                    messages.success(request, 'Registration successful!')
                
                return redirect('event_detail', pk=pk)
                
            except Exception as e:
                if 'UNIQUE constraint failed' in str(e):
                    messages.error(request, 'You are already registered for this event.')
                else:
                    messages.error(request, f'Registration failed: {str(e)}')
                return redirect('event_detail', pk=pk)
    else:
        form = RegistrationForm()
    
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'events/register.html', context)

@require_POST
def cancel_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.status = 'cancelled'
    event.save()
    messages.success(request, f'Event "{event.title}" has been cancelled.')
    return redirect('event_detail', pk=pk)

def event_statistics(request):
    events = Event.objects.annotate(
        registration_count=Count('registrations', filter=Q(registrations__status='confirmed'))
    )
    
    stats = {
        'total_events': events.count(),
        'active_events': events.filter(status='active').count(),
        'cancelled_events': events.filter(status='cancelled').count(),
        'total_registrations': Registration.objects.filter(status='confirmed').count(),
    }
    
    context = {
        'events': events,
        'stats': stats,
    }
    return render(request, 'events/statistics.html', context)