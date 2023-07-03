from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Event, Registration, Venue
from .models import User as CustomUser



class RegistrationInline(admin.TabularInline):
    model = Registration


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')
    actions = ['generate_attendee_list']
    inlines = [RegistrationInline]

    def generate_attendee_list(self, request, queryset):
        # Process the selected events to generate the attendee list
        # Customize this code based on your requirements
        pass

    generate_attendee_list.short_description = "Generate Attendee List"


class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'amenities', 'availability')


class CustomUserAdmin(UserAdmin):
    # Customize the UserAdmin class as per your requirements
    # You can add or remove fields to be displayed in the admin panel
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.register(Event, EventAdmin)
admin.site.register(Registration)
admin.site.register(Venue, VenueAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
