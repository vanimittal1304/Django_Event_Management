from rest_framework import serializers
from events.models import Event
from .models import Registration

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'capacity']

class RegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Registration
        fields = ['event', 'name', 'email', 'additional_details']
        
    def validate(self, data):
        event = self.context['event']
        name = data.get('name')
        email = data.get('email')
        
        # Perform field-level validations
        if not name:
            raise serializers.ValidationError("Name is required")
        if not email:
            raise serializers.ValidationError("Email is required")
        
        # Add any additional validations based on your requirements
        
        return data
