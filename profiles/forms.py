from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "bio", "profile_picture"]
    