import uuid

import uuid

from django.db import models
from django.conf import settings


class Event(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField(max_length=2000, blank=True)

    # This Meta class tells Django to always append ORDER BY date ASC to any SQL query on the 
    # Event table. So when the view calls Event.objects.all(), the database 
    # returns rows pre-sorted by date. Its handled by the database, not server
    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name