
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    token = models.CharField(max_length=200, blank=True, null=True)

