from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    daysoff = models.CharField(max_length=7, null=True, blank=True)
    days_worked = models.IntegerField(default=0)
    precentage = models.IntegerField(default=0)
    sum_precentage = models.IntegerField(default=0)
    salary = models.IntegerField(default=0, null=True)
    tardiness = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.username
