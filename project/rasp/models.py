from django.db import models


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
    dayOfWeek = models.CharField(max_length=30)
    skills_per_day = models.ManyToManyField(Skills_limits)

    def __int__(self):
        return self.day_num

class WeekendSetting(models.Model):
    weekendsPerWeek = models.IntegerField()

    def __int__(self):
        return self.weekendsPerWeek

class Users(models.Model):
    id_user = models.IntegerField(default=1)
    userName = models.CharField(max_length=30)
    daysoff = models.CharField(max_length=7)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.daysoff



