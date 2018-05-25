from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Company(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Skill(models.Model):
    nameSkill = models.CharField(max_length=30)

    def __str__(self):
        return self.nameSkill

class Skills_limits(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    sum_employee = models.IntegerField()
    name_skill = models.CharField(max_length=30, default=str(skill))

    def __str__(self):
        return self.name_skill

class Duty_setting(models.Model):
    day_num = models.IntegerField(default=1)
    day_name = models.CharField(max_length=30)
    skills_per_day = models.ManyToManyField(Skills_limits)

    def __str__(self):
        return self.day_name


class WeekendSetting(models.Model):
    weekendsPerWeek = models.IntegerField()

    def __int__(self):
        return self.weekendsPerWeek


class Users(models.Model):
    id_user = models.IntegerField(default=1)
    userName = models.CharField(max_length=30)
    daysoff = models.CharField(max_length=7)

    def __str__(self):
        return self.userName

class Rating(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user)


class DayResults(models.Model):
    date = models.DateField()
    income = models.IntegerField()
    day_num = models.IntegerField()

    def __str__(self):
        return str(self.date)

#@receiver('post_save', sender=DayResults)
#def update_rating(sender, instance, **kwargs):
#    instance.income
#    for res in instance.userdayresult_set
#        res.user

class UserDayResults(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    day = models.ForeignKey(DayResults, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)




