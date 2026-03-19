from django.db import models
from django.conf import settings

# Create your models here.
class MyS3Image(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "my_s3_image"
    )

    # documentation on this: https://docs.djangoproject.com/en/6.0/ref/models/fields/#django.db.models.FileField.upload_to
    image = models.ImageField(upload_to="images/mys3images/")
