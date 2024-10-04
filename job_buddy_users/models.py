from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class JobBuddyUser(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'    # Email authentication
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email 