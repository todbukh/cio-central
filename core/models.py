from django.contrib.auth.models import AbstractUser
from django.db import models

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

    def has_executive_role(self):
        return self.role in {self.Role.OWNER, self.Role.EXEC}

    def can_access_executive_panel(self):
        return self.has_executive_role() and self.status == self.Status.APPROVED

    def __str__(self):
        return self.username
