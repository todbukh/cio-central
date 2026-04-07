import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from core.permissions import is_executive, is_owner as check_is_owner
from project_a_17.settings import DELETED_USER_UID

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "OWNER"
        EXEC = "EXEC"
        MEMBER = "MEMBER"

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

    def __str__(self):
        return self.username

def get_deleted_user():
    return User.objects.get_or_create(
        uid=DELETED_USER_UID,
        defaults={
            "username": "deleted_user",
            "email": "deleted_user@ciocentral.com",
            "password": "blah",
            "first_name": "Deleted",
            "last_name": "User",
            "is_active": False,
            "status": "BANNED",
            "role": "MEMBER",
        })[0]