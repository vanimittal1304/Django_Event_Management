from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from events.models import Event, Registration
from events.serializers import EventSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import IsAdminUser



@api_view(['GET'])
def upcoming_events(request):
    paginator = CustomPagination()
    events = Event.objects.filter(date__gte=timezone.now())
    paginated_events = paginator.paginate_queryset(events, request)
    serializer = EventSerializer(paginated_events, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def filter_events(request):
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    date = request.GET.get('date')
    location = request.GET.get('location')

    events = Event.objects.all()

    if category:
        events = events.filter(category=category)
    if tag:
        events = events.filter(tags__contains=tag)
    if date:
        events = events.filter(date=date)
    if location:
        events = events.filter(location=location)

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def event_details(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def register(request):
    event_id = request.data.get('event_id')  # Assuming the client sends the event_id in the request data
    user = request.user  # Assuming you are using authentication and the participant is the authenticated user

    try:
        event = Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    if event.capacity <= event.registrations.count():
        return Response({'error': 'Event is already full'}, status=status.HTTP_400_BAD_REQUEST)

    registration = Registration(event=event, user=user)
    registration.save()

    serializer = RegistrationSerializer(registration)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def rsvp(request, event_id):
    user = request.user
    try:
        event = Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    registration, created = Registration.objects.get_or_create(event=event, user=user)

    if created:
        return Response({'message': 'RSVP successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'You have already RSVPed for this event'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Require authentication to access this view
def registration_history(request):
    user = request.user
    registrations = Registration.objects.filter(user=user)
    serializer = RegistrationSerializer(registrations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# New views for JWT authentication
@api_view(['POST'])
def obtain_token_pair(request):
    # Logic to obtain JWT token pair (access and refresh tokens)
    pass

@api_view(['POST'])
def refresh_token(request):
    # Logic to refresh the access token using the provided refresh token
    pass

class CustomPagination(PageNumberPagination):
    page_size = 10
