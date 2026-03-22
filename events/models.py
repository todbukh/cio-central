import uuid

from django.conf import settings
from django.db import models

# Events have the following fields:
# - UID (UUID, auto-generated, unique, non-editable)
# - Name (string)
# - Date (datetime)
# - Description (text)
# - Created by (foreign key to user, nullable)
class Event(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField(max_length=2000)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_events",
    )

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.name
