from rest_framework import generics
from django.shortcuts import render
from .serializers import EventSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from datetime import datetime
from django import forms
from .forms import EventForm
from .models import Event, Registration
from django.http import HttpResponse
from .models import Venue


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'capacity', 'categories']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < datetime.now().date():
            raise forms.ValidationError("Event date must be in the future.")
        return date

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user != event.creator:
        raise PermissionDenied("You do not have permission to edit this event.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user != event.creator:
        raise PermissionDenied("You do not have permission to delete this event.")

    if request.method == 'POST':
        event.delete()
        return redirect('event_list')

    return render(request, 'delete_event.html', {'event': event})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def manage_registrations(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(event=event)

    context = {
        'event': event,
        'registrations': registrations
    }

    return render(request, 'manage_registrations.html', context)

def accept_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    registration.status = 'accepted'
    registration.save()
    # You can add any additional logic or redirect to another page if needed
    return redirect('manage_registrations', event_id=registration.event.id)

def reject_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    registration.status = 'rejected'
    registration.save()
    # You can add any additional logic or redirect to another page if needed
    return redirect('manage_registrations', event_id=registration.event.id)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    context = {
        'event': event,
        'registrations_count': event.registrations.count()
    }

    return render(request, 'event_detail.html', context)

def generate_attendee_list(request, event_id):
    # Retrieve the event and its registrations
    event = Event.objects.get(pk=event_id)
    registrations = Registration.objects.filter(event=event)

    # Generate the attendee list or export the registration data
    # Customize this code based on your requirements

    # For example, you can create a CSV file with registration details
    csv_content = "Username,Email\n"
    for registration in registrations:
        csv_content += f"{registration.user.username},{registration.user.email}\n"

    # Create the HTTP response with the CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendee_list.csv"'
    response.write(csv_content)

    return response

def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'venue_list.html', {'venues': venues})

def venue_detail(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    upcoming_events = venue.get_upcoming_events()
    return render(request, 'venue_detail.html', {'venue': venue, 'upcoming_events': upcoming_events})

