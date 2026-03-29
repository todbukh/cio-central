from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User
from events.models import Event

# Create your models here.
class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT"
        ABSENT = "ABSENT"
        EXCUSED = "EXCUSED"
        UNSET = "UNSET"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['member', 'event'], name='unique_attendance')
        ]
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE) #FIXME: Talk to Quintin. This is a dummy model for now
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNSET)

    def __str__(self):
        return self.member.username