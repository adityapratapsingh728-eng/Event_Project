from django.db import models
from django.conf import settings

class UserMember(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=100)
    member_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20)

class CollegeData(models.Model):
    college_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    u_role = models.CharField( max_length=20)