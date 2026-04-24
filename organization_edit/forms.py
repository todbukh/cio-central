from django import forms
from .models import Organization


class OrganizationEditForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "organization_picture"]
