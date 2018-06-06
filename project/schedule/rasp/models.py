from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from schedule.users.models import Users


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



class Rating(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    value = models.FloatField(default=0)

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

    count = 0
    duty = Duty_setting.objects.all()

    def worked_change(day, user):
        worked = Users.objects.get(username=user)
        worked.days_worked += day
        worked.save()

    def rating_change(point, user, skill):
        rating = Rating.objects.get(user=user, skill=skill)
        rating.value += point
        rating.value = round(rating.value, 1)
        rating.save()

    def sum_percentage(value, user):
        sum = Users.objects.get(username=user)
        sum.sum_precentage += sum.precentage/100 * value
        sum.save()

    for user_day_result in UserDayResults.objects.all():
        if str(user_day_result.day) == str(instance.date):
            count += 1
    for user_day_result in UserDayResults.objects.all():
        if str(user_day_result.day) == str(instance.date):
            avg_price = duty.values_list('avg_income', flat=True).get(day_num=instance.day_num)
            if user_day_result.change_point_rating != 0:
                if user_day_result.change_point_rating > 0:
                    rating_change(-(user_day_result.change_point_rating), user_day_result.user, user_day_result.skill)
                if user_day_result.change_point_rating < 0:
                    rating_change(user_day_result.change_point_rating, user_day_result.user, user_day_result.skill)
                sum_percentage((-(user_day_result.change_point_rating * 10000 * count)), user_day_result.user)
                user_day_result.change_point_rating = 0
                user_day_result.save()
                worked_change(-1, user_day_result.user)
            if avg_price <= instance.income:
                user_day_result.change_point_rating += instance.income / count / 10000
                user_day_result.save()
                rating_change(user_day_result.change_point_rating, user_day_result.user, user_day_result.skill)
                sum_percentage(instance.income, user_day_result.user)
                worked_change(1, user_day_result.user)
            if avg_price > instance.income:
                user_day_result.change_point_rating -= instance.income / count / 10000
                user_day_result.save()
                rating_change(user_day_result.change_point_rating, user_day_result.user, user_day_result.skill)
                sum_percentage(instance.income, user_day_result.user)
                worked_change(1, user_day_result.user)



class UserDayResults(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    day = models.ForeignKey(DayResults, on_delete=models.CASCADE)
    change_point_rating = models.FloatField(default=0)

    def __str__(self):
        return str(self.user)





