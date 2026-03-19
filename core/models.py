from django.contrib.auth.models import AbstractUser
from django.db import models
from core.permissions import is_executive, is_owner

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

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def is_owner(self): # FIXME: look into permissions.py
        return is_owner(self)

    def __str__(self):
        return self.username

    def is_exec(self):
        return is_executive(self)
