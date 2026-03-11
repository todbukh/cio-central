from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(blank=True)
    # profile_picture = ...  add later when ready for file uploads

    def __str__(self):
        return f"Profile of {self.user.username}"
