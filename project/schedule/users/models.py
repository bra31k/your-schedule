from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    daysoff = models.CharField(max_length=7, null=True)
    days_worked = models.IntegerField(default=0)
    precentage = models.IntegerField(default=0)
    sum_precentage = models.IntegerField(default=0)
    salary = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.username
