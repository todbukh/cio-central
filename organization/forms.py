from django import forms

class MessageForm(forms.Form):
    text = forms.CharField(max_length=2000)