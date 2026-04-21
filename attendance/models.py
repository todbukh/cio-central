from django.db import models

from core.models import User, get_deleted_user
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
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNSET)

    def __str__(self):
        return self.member.username