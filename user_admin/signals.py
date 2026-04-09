# Generated in part by Claude Opus 4.6 Extended
from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.models import User
from attendance.models import Attendance

# this deletes all the attendance records for a user admin upon their promotion to the role
@receiver(pre_save, sender=User)
def delete_user_admin_attendance_on_promotion(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return
    if old.role != User.Role.USERADMIN and instance.role == User.Role.USERADMIN:
        Attendance.objects.filter(member=instance).delete()
