from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    # Override date field to use the browser's datetime-local input
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Event
        fields = ["name", "date", "description"]
