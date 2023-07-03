from django.urls import path
from . import views
from .views import RegistrationAPIView
from participants.views import upcoming_events, filter_events, event_details, register
from .views import RegisterAPIView, ObtainTokenPairAPIView, RefreshTokenAPIView
from participants.views import upcoming_events, register, rsvp, registration_history


app_name = 'participants'

urlpatterns = [
    path('participants/register/', RegistrationAPIView.as_view(), name='register'),
    path('upcoming-events/', upcoming_events, name='upcoming-events'),
    path('filter-events/', filter_events, name='filter-events'),
    path('event-details/<int:event_id>/', event_details, name='event-details'),
    path('register/', register, name='register'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/', ObtainTokenPairAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenAPIView.as_view(), name='token_refresh'),
    path('rsvp/<int:event_id>/', views.rsvp, name='rsvp'),
    path('registration-history/', views.registration_history, name='registration_history'),
    path('upcoming-events/', upcoming_events, name='upcoming-events'),
    path('register/', register, name='register'),
    path('rsvp/<int:event_id>/', rsvp, name='rsvp'),
    path('registration-history/', registration_history, name='registration-history'),
]
