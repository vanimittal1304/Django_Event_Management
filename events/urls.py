from django.urls import path
from . import views


app_name = 'events'

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),

    # Registration management URLs
    path('events/<int:event_id>/registrations/', views.manage_registrations, name='manage_registrations'),
    path('events/registrations/<int:registration_id>/accept/', views.accept_registration, name='accept_registration'),
    path('events/registrations/<int:registration_id>/reject/', views.reject_registration, name='reject_registration'),
    path('<int:event_id>/attendee_list/', views.generate_attendee_list, name='attendee_list'),
    path('venues/', views.venue_list, name='venue_list'),
    path('venues/<int:venue_id>/', views.venue_detail, name='venue_detail'),
]
