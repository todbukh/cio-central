from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, error_messages={"required": "First name cannot be empty."})
    last_name = forms.CharField(max_length=150, error_messages={"required": "Last name cannot be empty."})
    
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "bio", "profile_picture"]
    