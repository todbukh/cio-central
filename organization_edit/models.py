from django.db import models

# Create your models here.
class Organization(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    name = models.CharField(max_length=20, default="My Organization")
    organization_picture = models.ImageField(upload_to="images/organization-edit/", blank=True, null=True)
