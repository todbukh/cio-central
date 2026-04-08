import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from core.permissions import is_executive, is_user_admin, is_owner as check_is_owner

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "OWNER"
        EXEC = "EXEC"
        MEMBER = "MEMBER"
        USERADMIN = "USERADMIN"

    class Status(models.TextChoices):
        PENDING = "PENDING"
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"
        BANNED = "BANNED"

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def is_exec(self):
        return is_executive(self)

    def is_owner(self):
        return check_is_owner(self)

    def is_user_admin(self):
        return is_user_admin(self)

    def __str__(self):
        return self.username
