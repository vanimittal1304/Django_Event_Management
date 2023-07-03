from django import forms
from .models import Event
from datetime import datetime

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'capacity', 'categories']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < datetime.now().date():
            raise forms.ValidationError("Event date must be in the future.")
        return date
