from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class Advisor(models.Model):
    advName = models.CharField(max_length=100)
    imgURL = models.URLField()

class User(AbstractUser):
    username = None
    uName = models.CharField(max_length=100)
    uEmail = models.EmailField(max_length=100, unique=True)    

    USERNAME_FIELD = 'uEmail'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Bookings(models.Model):
    time = models.DateTimeField()
    uID = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    aID = models.ForeignKey('Advisor', on_delete=models.DO_NOTHING)
