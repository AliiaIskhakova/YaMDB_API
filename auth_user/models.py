from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(choices=Role.choices, default=Role.USER,
                            max_length=500)
    email = models.EmailField(unique=True,
                              error_messages={'unique': 'This email exists'})
    confirmation_code = models.CharField(max_length=11)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
