from django.forms import Form
from django.forms.fields import ImageField


class S3Form(Form):
    image = ImageField(label="Upload Your S3 Image Here", required=True)