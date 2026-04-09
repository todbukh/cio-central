# Generated in part by Claude Opus 4.6 Extended
from django.db.models.signals import pre_save
from django.dispatch import receiver
from attendance.models import Attendance
from profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


# this deletes all the attendance records for a user admin upon their promotion to the role
@receiver(pre_save, sender=User)
def delete_user_admin_attendance_and_profile_on_promotion(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return
    if old.role != User.Role.USERADMIN and instance.role == User.Role.USERADMIN:
        Attendance.objects.filter(member=instance).delete()
        Profile.objects.filter(user=instance).delete()
