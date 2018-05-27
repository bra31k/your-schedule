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
    avg_income = models.IntegerField(default=1)
    worked_hours_in_day = models.IntegerField(default=8)

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
    days_worked = models.IntegerField(default=0)

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


@receiver(post_save, sender=DayResults)
def update_rating(sender, instance, **kwargs):
    instance.income
    instance.date
    count = 0
    duty = Duty_setting.objects.all()
    for user_day_result in UserDayResults.objects.all():
        if str(user_day_result.day) == str(instance.date):
            count += 1
    for user_day_result in UserDayResults.objects.all():
        if str(user_day_result.day) == str(instance.date):
            avg_price = duty.values_list('avg_income', flat=True).get(day_num=instance.day_num)
            if avg_price <= instance.income:
                rating = Rating.objects.get(user=user_day_result.user, skill=user_day_result.skill)
                rating.value += instance.income / count / 10000
                rating.save()
                worked = Users.objects.get(userName=user_day_result.user)
                worked.days_worked += 1
                worked.save()
            if avg_price > instance.income:
                rating = Rating.objects.get(user=user_day_result.user, skill=user_day_result.skill)
                rating.value -= instance.income / count / 10000
                rating.save()
                worked = Users.objects.get(userName=user_day_result.user)
                worked.days_worked += 1
                worked.save()



class UserDayResults(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    day = models.ForeignKey(DayResults, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)




