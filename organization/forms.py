from django import forms

from organization.models import Channel


class MessageForm(forms.Form):
    text = forms.CharField(max_length=2000, required=True)

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        exclude = ["builtin"]

        labels = {
            "name": "Channel Name"
        }

        error_messages = {
            "name": {
                "unique": "A channel with that name already exists.",
            }
        }