from django import forms
from .models import Event

# Right now here are the field contraints
# - name: required, max_length=64
# - date: required, must be a valid datetime
# - location: optional, max_length=100
# - description: optional, max_length=2000

class EventForm(forms.ModelForm):
    name = forms.CharField(
        max_length=64,
        required=True,
        error_messages={
            "required": "Event name is required.",
            "max_length": "Event name cannot exceed 64 characters.",
        }
    )

    location = forms.CharField(
        max_length=100,
        required=False,
        error_messages={"max_length": "Address cannot exceed 100 characters."}
    )

    description = forms.CharField(
        max_length=2000,
        required=False,
        error_messages={"max_length": "Description cannot exceed 2000 characters."}
    )

    # Override date field to use the browser's datetime-local input
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M"]
    )

    class Meta:
        model = Event
        fields = ["name", "date", "location", "description"]
