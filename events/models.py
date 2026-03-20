import uuid

from django.db import models
from django.conf import settings

# Create your models here.
class Event(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name