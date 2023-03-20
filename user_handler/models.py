from django.db import models
from django.contrib.auth.models import AbstractUser
from django import utils


class User(AbstractUser):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=500)
    is_logged = models.BooleanField(default=False)

    def __str__(self):
        return self.username