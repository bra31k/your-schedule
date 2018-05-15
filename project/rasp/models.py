from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Skill(models.Model):
    nameSkill = models.CharField(max_length=30)

    def __str__(self):
        return self.nameSkill

class SkillPerDay(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    employee_in_day = models.IntegerField()
    name_skill = models.CharField(max_length=30, default=str(skill))

    def __str__(self):
        return self.name_skill

class DaysOff(models.Model):
    dayOfWeek = models.CharField(max_length=30)
    skills_per_day = models.ManyToManyField(SkillPerDay)

    def __str__(self):
        return self.dayOfWeek

class WeekendSetting(models.Model):
    weekendsPerWeek = models.IntegerField()

    def __int__(self):
        return self.weekendsPerWeek

class PersonalVotes(models.Model):
    userName = models.CharField(max_length=30)
    selected_day = models.CharField(max_length=7)
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.selected_day



