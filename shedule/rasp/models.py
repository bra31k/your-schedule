from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class DaysOff(models.Model):
    dayOfWeek = models.CharField(max_length=30)
    employeeInDay = models.IntegerField()
    def __str__(self):
        return self.dayOfWeek

class WeekendSetting(models.Model):
    weekendsPerWeek = models.IntegerField()
    def __str__(self):
        return self.weekendsPerWeek

class PersonalVotes(models.Model):
    userName = models.CharField(max_length=30)
    selected_day = models.CharField(max_length=7)
# Create your models here.
