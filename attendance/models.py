from django.db import models
from django.db.models import Q

from core.models import User, get_deleted_user
from events.models import Event
from project_a_17.settings import DELETED_USER_UID


# Create your models here.
class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT"
        ABSENT = "ABSENT"
        EXCUSED = "EXCUSED"
        UNSET = "UNSET"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['member', 'event'], condition=~Q(user_uid=DELETED_USER_UID), name='unique_attendance')
        #   # FIXME: We should talk about this. See also polls model line 64.
        ]
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNSET)

    def __str__(self):
        return self.member.username