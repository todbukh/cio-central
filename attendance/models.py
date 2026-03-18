from django.db import models
from core.models import User
from events.models import Event

# Create your models here.
class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT"
        ABSENT = "ABSENT"
        EXCUSED = "EXCUSED"
        UNSET = "UNSET"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE) #FIXME: Talk to Quintin. This is a dummy model for now
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNSET)
